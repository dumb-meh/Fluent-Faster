import os
import json
import time
import uuid
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
from .pronunciation_schema import pronunciation_response, pronunciation_request
from app.utils.text_to_speech import generate_tts_direct,get_language_code, ThreadSafeCounter

load_dotenv()

counter = ThreadSafeCounter()
class Pronunciation:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def get_pronunciation(self, input_data: pronunciation_request) -> List[pronunciation_response]:
        try:
            prompt = self.create_prompt()
            full_prompt = f"{prompt}\n\nInput: {input_data}"
            response = self.model.generate_content(full_prompt)
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
                target_language_code = get_language_code(input_data.language)
                    
                english_task = {
                    'text': item['english'],
                    'language': 'en-US',
                    'voice_name': 'en-US-AvaMultilingualNeural',
                    'unique_id': f"{base_timestamp}_{counter_val}_{i}_en"
                }
                    
                target_task = {
                    'text': item['target_language'],
                    'language': target_language_code,
                    'voice_name': 'en-US-AvaMultilingualNeural',
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
                        audio_url = generate_tts_direct(task, "pronunciation")
                        
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

        
    
    def create_prompt(self) -> str:
        return """You are a language learning assistant that creates pronunciation practice sentences. Your task is to generate sentences in a target language using provided English words, calibrated to a specific speaking duration.

                INPUT:
                - words: English words (as a string)
                - time_length: Target duration for pronouncing all sentences (e.g., "30 seconds", "2 minutes")
                - language: Target language for sentence creation

                OUTPUT: A list of sentence pairs in the target language that:
                1. Incorporate ALL the provided English words naturally
                2. Are grammatically correct in the target language
                3. Have a total speaking time that matches the requested time_length
                4. Are appropriate for pronunciation practice
                5. Include both the target language sentence AND its English translation for comprehension

                TIMING GUIDELINES:
                - Average speaking pace: ~150-180 words per minute (2.5-3 words per second)
                - Adjust sentence complexity based on target language difficulty
                - For beginners: slower pace, simpler sentences
                - For advanced: normal pace, more complex structures

                SENTENCE CREATION RULES:
                1. Use each English word at least once across all sentences
                2. Create natural, meaningful sentences (avoid forced word combinations)
                3. Vary sentence length and structure for engaging practice
                4. Include a mix of:
                - Simple declarative sentences
                - Questions
                - Compound sentences (when appropriate)
                5. Ensure sentences flow logically when read together
                6. Make sentences relevant and interesting to maintain engagement

                LANGUAGE-SPECIFIC CONSIDERATIONS:
                - Adapt to target language grammar and syntax
                - Use appropriate verb tenses and conjugations
                - Include relevant cultural context when natural
                - For languages with different word order, prioritize natural flow over literal translation

                QUALITY CHECKS:
                - Verify all English words are used
                - Estimate total speaking time matches request
                - Ensure grammatical accuracy
                - Check for natural pronunciation flow

                EXAMPLE OUTPUT FORMAT:
                [
                    {"target_language": "Sentence 1 in target language", "english": "Sentence 1 in English"},
                    {"target_language": "Sentence 2 in target language", "english": "Sentence 2 in English"},
                    {"target_language": "Sentence 3 in target language", "english": "Sentence 3 in English"}
                ]

                Now generate pronunciation practice sentences using the provided words, target duration, and language."""