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
import io

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
            
            if not azure_key or not azure_region:
                return ""

            token_endpoint = f"https://{azure_region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
            tts_endpoint = f"https://{azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
            
            headers = {"Ocp-Apim-Subscription-Key": azure_key}
            token_response = requests.post(token_endpoint, headers=headers, timeout=10)
            
            if token_response.status_code != 200:
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
                return ""
            
            client = storage.Client()
            bucket_name = os.getenv("BUCKET_NAME")
            
            if not bucket_name:
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
            
        except Exception:
            return ""
    
def get_language_code(self, language: str) -> str:
        """
        Convert language names to proper language codes
        """
        language_mapping = {
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
