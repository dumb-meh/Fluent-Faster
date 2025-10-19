from fastapi import APIRouter, HTTPException, Body
import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

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
            "Respond ONLY with a valid JSON object using this exact structure:\n"
            '{ "target_language": "New sentence in original language", "english": "Translation in English" }'
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

            english_task = {
                    'text': data['english'],
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
                    
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Could not parse model output as JSON: {output}")

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
