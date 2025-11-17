from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import uuid
import time
import threading
from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime, timedelta
import google.generativeai as genai
import json
import re
from typing import List

router = APIRouter()
load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

TOKEN_ENDPOINT = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
TTS_ENDPOINT = f"https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"


class TTSRequest(BaseModel):
    text: str
    language: str = "en-US"
    voice_name: str = "en-US-ChristopherNeural"
    gender: str = "Male"


class TranslationVoiceRequest(BaseModel):
    sentence_list: List[str]
    base_language: str
    target_language: str


def get_token(subscription_key: str) -> str:
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    response = requests.post(TOKEN_ENDPOINT, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch token: {response.text}")
    return response.text

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def get_next(self):
        with self._lock:
            self._value += 1
            return self._value

def generate_tts_direct(task: dict, feature) -> str:
    """
    Generate TTS directly using Azure Speech API (no HTTP calls)
    """
    try:
        azure_key = os.getenv("AZURE_SPEECH_KEY")
        azure_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not azure_key:
            print("AZURE_SPEECH_KEY not found")
            return ""
        if not azure_region:
            print("AZURE_SPEECH_REGION not found")
            return ""

        token_endpoint = f"https://{azure_region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        tts_endpoint = f"https://{azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        
        headers = {"Ocp-Apim-Subscription-Key": azure_key}
        token_response = requests.post(token_endpoint, headers=headers, timeout=10)
        
        if token_response.status_code != 200:
            print(f"Token request failed with status {token_response.status_code}: {token_response.text}")
            return ""
        
        token = token_response.text

        ssml = f"""
        <speak version='1.0' xml:lang='{task['language']}'>
            <voice xml:lang='{task['language']}' xml:gender='Female' name='{task['voice_name']}'>
                {task['text']}
            </voice>
        </speak>
        """

        tts_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "fastapi-tts-app"
        }
        
        tts_response = requests.post(tts_endpoint, headers=tts_headers, data=ssml.encode("utf-8"), timeout=15)
        
        if tts_response.status_code != 200:
            print(f"TTS request failed with status {tts_response.status_code}: {tts_response.text}")
            return ""
        
        client = storage.Client()
        bucket_name = os.getenv("BUCKET_NAME")
        
        if not bucket_name:
            print("BUCKET_NAME not found")
            return ""
        
        bucket = client.bucket(bucket_name)
        
        timestamp = str(int(time.time() * 1000))
        unique_id = str(uuid.uuid4())[:12]
        filename = f"temp_audio_file/{feature}_{timestamp}_{unique_id}.wav"

        blob = bucket.blob(filename)
        blob.upload_from_string(
            tts_response.content,
            content_type="audio/wav"
        )
        
        encoded_filename = filename.replace("/", "%2F")
        audio_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/{encoded_filename}?alt=media"
        
        return audio_url
        
    except Exception as e:
        # Store error in a way that can be accessed by calling function
        error_msg = f"TTS Direct Error: {str(e)} | Type: {type(e).__name__}"
        # You could also log to a file or external service here
        print(error_msg)  # Keep this for local debugging
        return ""

def get_language_code(language: str) -> str:
    """
    Convert language names to proper language codes
    """
    language_mapping = {
        "english": "en-US",
        "spanish": "es-ES",
        "french": "fr-FR",
        "german": "de-DE", 
        "italian": "it-IT",
        "portuguese": "pt-BR",
        "japanese": "ja-JP",
        "korean": "ko-KR",
        "chinese": "zh-CN",
        "russian": "ru-RU",
        "arabic": "ar-SA"
    }
    
    if "-" in language:
        return language
        
    return language_mapping.get(language.lower(), "es-ES")

def get_voice_name(language: str) -> str:
    """
    Get the appropriate voice name for a given language
    """
    voice_mapping = {
        "english": "en-US-AvaMultilingualNeural",
        "chinese": "zh-CN-XiaoxiaoMultilingualNeural",
        "spanish": "es-MX-JorgeMultilingualNeural",
        "french": "fr-FR-Remy:DragonHDLatestNeural",
        "german": "de-DE-Florian:DragonHDLatestNeural",
        "italian": "it-IT-GiuseppeMultilingualNeural",
        "japanese": "ja-JP-Masaru:DragonHDLatestNeural",
        "portuguese": "pt-BR-ThalitaMultilingualNeural",
        "arabic": "ar-SA-HamedNeural",
    }
    
    # Return specific voice if language is mapped, otherwise default to AvaMultilingualNeural
    return voice_mapping.get(language.lower(), "en-US-AvaMultilingualNeural")


@router.post("/text_to_speech")
async def text_to_speech(request: TTSRequest):
    try:
        token = get_token(AZURE_SPEECH_KEY)

        ssml = f"""
        <speak version='1.0' xml:lang='{request.language}'>
            <voice xml:lang='{request.language}' xml:gender='{request.gender}' name='{request.voice_name}'>
                {request.text}
            </voice>
        </speak>
        """

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "fastapi-tts-app"
        }

        response = requests.post(TTS_ENDPOINT, headers=headers, data=ssml.encode("utf-8"))

        if response.status_code == 200:
            try:
                client = storage.Client()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to initialize GCS client: {str(e)}")
            
            bucket_name = os.getenv("BUCKET_NAME")
            if not bucket_name:
                raise HTTPException(status_code=500, detail="BUCKET_NAME environment variable not set")
            
            bucket = client.bucket(bucket_name)
            
            timestamp = str(int(time.time() * 1000))  # Use milliseconds for better uniqueness
            unique_id = str(uuid.uuid4())[:12]  # Longer unique ID
            filename = f"temp_audio_file/tts_{timestamp}_{unique_id}.wav"
            
            blob = bucket.blob(filename)
            blob.upload_from_string(
                response.content,
                content_type="audio/wav"
            )
            
            encoded_filename = filename.replace("/", "%2F")
            audio_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/{encoded_filename}?alt=media"
            
            return {"audio_url": audio_url, "filename": filename.split("/")[-1]}
        else:
            raise HTTPException(status_code=response.status_code, detail=f"TTS request failed: {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translation_voice_generation")
async def translation_voice_generation(request: TranslationVoiceRequest):
    """
    Translate a list of sentences and generate audio for both original and translated versions
    """
    try:
        # Configure Gemini AI
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Join sentences into a single text for translation
        sentences_text = "\n".join(request.sentence_list)
        
        prompt = f"""You are a professional translator. Translate the following sentences from {request.base_language} to {request.target_language}.

Original sentences:
{sentences_text}

Provide the translation maintaining the same number of sentences and similar meaning. Return the result as a JSON object with this exact format:
{{"translated_sentences": ["sentence 1", "sentence 2", "sentence 3", ...]}}

Translated sentences:"""

        # Get translation from Gemini
        response = model.generate_content(prompt)
        raw_output = response.text.strip()
        
        # Extract JSON from response
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in the model response.")
        
        translation_json = json.loads(match.group(0))
        translated_sentences = translation_json.get('translated_sentences', [])
        
        if len(translated_sentences) != len(request.sentence_list):
            raise ValueError("Translation returned different number of sentences")
        
        # Initialize counter for unique file naming
        counter = ThreadSafeCounter()
        result = []
        
        # Process each sentence pair
        for i, (original, translated) in enumerate(zip(request.sentence_list, translated_sentences)):
            base_timestamp = int(time.time())
            counter_val = counter.get_next()
            
            # Get language codes and voice names
            base_language_code = get_language_code(request.base_language)
            target_language_code = get_language_code(request.target_language)
            base_voice_name = get_voice_name(request.base_language)
            target_voice_name = get_voice_name(request.target_language)
            
            # Create TTS tasks
            original_task = {
                'text': original,
                'language': base_language_code,
                'voice_name': base_voice_name,
                'unique_id': f"{base_timestamp}_{counter_val}_{i}_orig"
            }
            
            translated_task = {
                'text': translated,
                'language': target_language_code,
                'voice_name': target_voice_name,
                'unique_id': f"{base_timestamp}_{counter_val}_{i}_trans"
            }
            
            # Generate audio for both versions
            original_audio_url = ""
            translated_audio_url = ""
            
            try:
                original_audio_url = generate_tts_direct(original_task, "translation")
            except Exception as e:
                print(f"Failed to generate audio for original sentence {i}: {str(e)}")
            
            try:
                translated_audio_url = generate_tts_direct(translated_task, "translation")
            except Exception as e:
                print(f"Failed to generate audio for translated sentence {i}: {str(e)}")
            
            result.append({
                'original_sentence': original,
                'translated_sentence': translated,
                'original_audio_url': original_audio_url,
                'translated_audio_url': translated_audio_url
            })
        
        return {
            'base_language': request.base_language,
            'target_language': request.target_language,
            'sentence_pairs': result
        }
        
    except Exception as e:
        print(f"Translation voice generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))