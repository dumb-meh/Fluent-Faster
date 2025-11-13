import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from app.utils.text_to_speech import generate_tts_direct,get_language_code, get_voice_name, ThreadSafeCounter
from .recall_schema import recall_response, recall_request
from typing import List
import time
import requests
import threading
import uuid
from google.cloud import storage

load_dotenv()

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
                target_voice_name = get_voice_name(input_data.language)
                

                
                english_task = {
                    'text': item['english'],
                    'language': 'en-US',
                    'voice_name': 'en-US-AvaMultilingualNeural',
                    'unique_id': f"{base_timestamp}_{counter_val}_{i}_en"
                }
                
                target_task = {
                    'text': item['target_language'],
                    'language': target_language_code,
                    'voice_name': target_voice_name,
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
            

            
            for task_type, task, index in tts_tasks:
                    
                    audio_url = generate_tts_direct(task,"recall")
                    
                    if audio_url:
                        if task_type == 'english':
                            result[index]['english_url'] = audio_url
                        else:
                            result[index]['target_language_url'] = audio_url

            
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
    


