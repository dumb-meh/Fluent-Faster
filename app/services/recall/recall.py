import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .recall_schema import recall_response, recall_request
from typing import List
import time
import requests
import threading
import uuid
from google.cloud import storage

load_dotenv()


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def get_next(self):
        with self._lock:
            self._value += 1
            return self._value

counter = ThreadSafeCounter()

class Recall:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def get_recall(self, input_data: recall_request) -> List[recall_response]:
        try:
            prompt = self.create_prompt()
            full_prompt = f"{prompt}\n\nInput: words: {input_data.words}, language: {input_data.language}, number_of_sentences: {input_data.number_of_sentences}"
            response = self.model.generate_content(full_prompt)
            print(response.text)
            text = response.text
            if text.startswith("```json"):
                text = text[len("```json"):].strip()
            elif text.startswith("```"):
                text = text[len("```"):].strip()
            if text.endswith("```"):
                text = text[:-3].strip()
            data = json.loads(text)
            
            result = []
            tts_tasks = []
            
            for i, item in enumerate(data):
                base_timestamp = int(time.time())
                counter_val = counter.get_next()
                target_language_code = self.get_language_code(input_data.language)
                
                english_task = {
                    'text': item['english'],
                    'language': 'en-US',
                    'voice_name': 'en-US-ChristopherNeural',
                    'unique_id': f"{base_timestamp}_{counter_val}_{i}_en"
                }
                
                target_task = {
                    'text': item['target_language'],
                    'language': target_language_code,
                    'voice_name': self.get_voice_for_language(target_language_code),
                    'unique_id': f"{base_timestamp}_{counter_val}_{i}_tg"
                }
                
                tts_tasks.append(('english', english_task, i))
                tts_tasks.append(('target', target_task, i))
                
                result.append({
                    'target_language': item['target_language'],
                    'english': item['english'],
                    'english_url': '',
                    'target_language_url': ''
                })
            
            # Process TTS requests sequentially
            for task_type, task, index in tts_tasks:
                try:
                    audio_url = self.call_tts_endpoint(task)
                    
                    if audio_url:
                        if task_type == 'english':
                            result[index]['english_url'] = audio_url
                        else:
                            result[index]['target_language_url'] = audio_url
                        
                except Exception as e:
                    print(f"TTS failed for {task_type} at index {index}: {str(e)}")
            
            return result
            
        except Exception as e:
            # If we have data but TTS failed, return the sentences anyway
            if 'data' in locals() and data:
                result = []
                for item in data:
                    result.append({
                        'target_language': item['target_language'],
                        'english': item['english'],
                        'english_url': '',
                        'target_language_url': ''
                    })
                return result
            else:
                return [{
                    'target_language': 'Error occurred',
                    'english': 'Error occurred', 
                    'english_url': '',
                    'target_language_url': ''
                }]
    
    def call_tts_endpoint(self, task: dict) -> str:
        """
        Generate TTS directly using Azure Speech API
        """
        try:
            return self.generate_tts_direct(task)
        except Exception:
            return ""

    def generate_tts_direct(self, task: dict) -> str:
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
                <voice xml:lang='{task['language']}' xml:gender='Male' name='{task['voice_name']}'>
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
            filename = f"temp_audio_file/recall_{timestamp}_{unique_id}.wav"

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
    
    def get_voice_for_language(self, language: str) -> str:
        """
        Map language codes to appropriate Azure Speech voices
        """
        voice_mapping = {
            "es": "es-ES-AlvaroNeural",
            "es-ES": "es-ES-AlvaroNeural",
            "spanish": "es-ES-AlvaroNeural",
            "fr": "fr-FR-HenriNeural",
            "fr-FR": "fr-FR-HenriNeural",
            "french": "fr-FR-HenriNeural",
            "de": "de-DE-ConradNeural",
            "de-DE": "de-DE-ConradNeural",
            "german": "de-DE-ConradNeural",
            "it": "it-IT-DiegoNeural",
            "it-IT": "it-IT-DiegoNeural",
            "italian": "it-IT-DiegoNeural",
            "pt": "pt-BR-AntonioNeural",
            "pt-BR": "pt-BR-AntonioNeural",
            "portuguese": "pt-BR-AntonioNeural",
            "ja": "ja-JP-KeitaNeural",
            "ja-JP": "ja-JP-KeitaNeural",
            "japanese": "ja-JP-KeitaNeural",
            "ko": "ko-KR-InJoonNeural",
            "ko-KR": "ko-KR-InJoonNeural",
            "korean": "ko-KR-InJoonNeural",
            "zh": "zh-CN-YunxiNeural",
            "zh-CN": "zh-CN-YunxiNeural",
            "chinese": "zh-CN-YunxiNeural",
            "ru": "ru-RU-DmitryNeural",
            "ru-RU": "ru-RU-DmitryNeural",
            "russian": "ru-RU-DmitryNeural",
            "ar": "ar-SA-HamedNeural",
            "ar-SA": "ar-SA-HamedNeural",
            "arabic": "ar-SA-HamedNeural"
        }
        return voice_mapping.get(language.lower(), "en-US-ChristopherNeural")


    
    def create_prompt(self) -> str:
        return """You are a language learning assistant that creates recall practice sentences. Your task is to generate a specific number of sentences in a target language using provided English words to help users practice vocabulary recall and retention.

                INPUT:
                - words: English words (as a string)
                - language: Target language for sentence creation
                - number of sentences: Exact number of sentences to create (e.g., "5", "8", "12")

                OUTPUT: A list of sentence pairs in the target language that:
                1. Incorporate ALL the provided English words naturally across the sentences
                2. Are grammatically correct in the target language
                3. Match the exact number of sentences requested
                4. Are appropriate for vocabulary recall practice
                5. Include both the target language sentence AND its English translation for comprehension

                SENTENCE CREATION RULES:
                1. Distribute all English words across the requested number of sentences
                2. Each word should appear at least once, but words can be repeated if natural
                3. Create meaningful, contextually relevant sentences
                4. Vary sentence complexity and structure for engaging practice
                5. Include a mix of:
                - Simple declarative sentences
                - Questions
                - Compound sentences (when appropriate)
                - Different tenses and grammatical structures
                6. Ensure sentences are memorable and aid vocabulary retention
                7. Make sentences interconnected when possible (tell a story or relate to a theme)

                LANGUAGE-SPECIFIC CONSIDERATIONS:
                - Adapt to target language grammar and syntax
                - Use appropriate verb tenses and conjugations
                - Include relevant cultural context when natural
                - For languages with different word order, prioritize natural flow
                - Consider language-specific pronunciation challenges

                RECALL OPTIMIZATION:
                - Create sentences that help cement word meanings in memory
                - Use vivid, descriptive language when possible
                - Include emotional or memorable contexts
                - Vary the role each English word plays in different sentences
                - Make connections between words when logical

                QUALITY CHECKS:
                - Verify all English words are used appropriately
                - Confirm exact sentence count matches request
                - Ensure grammatical accuracy in both languages
                - Check for natural flow and meaningful content

                EXAMPLE OUTPUT FORMAT:
                [
                    {"target_language": "Sentence 1 in target language", "english": "Sentence 1 in English"},
                    {"target_language": "Sentence 2 in target language", "english": "Sentence 2 in English"},
                    {"target_language": "Sentence 3 in target language", "english": "Sentence 3 in English"}
                ]

                Return only the JSON list in the exact format shown above, without any additional text, explanations, or formatting."""
    


