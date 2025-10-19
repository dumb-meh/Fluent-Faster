from fastapi import APIRouter, HTTPException, Body
import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from app.utils.text_to_speech import generate_tts_direct, get_language_code

router = APIRouter()
load_dotenv()

@router.post("/regenerate_sentence")
async def regenerate_sentence(request_data: str = Body(..., media_type="text/plain")):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = (
            "You will be given a sentence in a foreign language.\n"
            "Your task is to rewrite the sentence to make it more advanced or complex, and then provide an English translation of the new version.\n"
            "Respond ONLY with a valid JSON object using this exact structure:\n. The original language should be the same as the input language and must be written in lowercase.\n"
            '{ "target_language": "New sentence in original language", "english": "Translation in English" ,"original_language":"spanish"}'
        )

        full_prompt = f"{prompt}\n\nInput: {request_data}"
        response = model.generate_content(full_prompt)

        output = response.text.strip()
        if output.startswith("```"):
            output = output.strip("`")  
            lines = output.splitlines()
            if lines[0].startswith("json"):
                lines = lines[1:]  
            output = "\n".join(lines).strip()


        try:
            data= json.loads(output)
            tts_tasks = []
            base_timestamp = int(time.time())



            target_language_code = get_language_code(data['original_language'])


            english_task = {
                    'text': data['english'],
                    'language': 'en-US',
                    'voice_name': 'en-US-AvaMultilingualNeural',
                    'unique_id': f"{base_timestamp}_en"
                }
                    
            target_task = {
                    'text': data['target_language'],
                    'language': target_language_code,
                    'voice_name': 'en-US-AvaMultilingualNeural',
                    'unique_id': f"{base_timestamp}_tg"
                }

            result = {
                    'target_language': data['target_language'],
                    'english': data['english'],
                    'english_url': '',
                    'target_language_url': ''
                }
            tts_tasks.append(('english', english_task))
            tts_tasks.append(('target', target_task))
            
            
            for task_type, task in tts_tasks:
                    try:
                        audio_url = generate_tts_direct(task, "regenerate_sentence")
                        
                        if audio_url:
                            if task_type == 'english':
                                result['english_url'] = audio_url
                            else:
                                result['target_language_url'] = audio_url

                    except Exception as e:
                        pass

            
            return result
                    
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Could not parse model output as JSON: {output}")

    except Exception as e:
        error_result = {
            'target_language': 'Error occurred',
            'english': 'Error occurred',
            'english_url': '',
            'target_language_url': ''
        }
        return error_result
