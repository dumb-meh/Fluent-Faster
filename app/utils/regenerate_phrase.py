from fastapi import APIRouter, HTTPException, Body
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

router = APIRouter()
load_dotenv()

@router.post("/regenerate_phrase")
async def regenerate_sentence(request_data: str = Body(..., media_type="text/plain")):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = (
            "You will be given a sentence.\n"
            "Your task is to generate a new sentence of that same topic.\n"
            "Respond ONLY with a valid JSON object using this exact structure:\n"
            '{ "foreign": "New sentence in original language", "english": "Translation in English" }'
        )

        full_prompt = f"{prompt}\n\nInput: {request_data}"
        response = model.generate_content(full_prompt)

        output = response.text.strip()
       
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
