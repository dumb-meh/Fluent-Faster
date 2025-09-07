from fastapi import APIRouter, HTTPException, Form
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

router = APIRouter()
load_dotenv()

@router.post("/translate")
async def translate_text(
    text: str = Form(...),
    language: str = Form(...)
):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = (
            f"You are a translation assistant.\n"
            f"Translate the following sentence to {language}.\n"
            f"Return ONLY the translation in JSON format like this:\n"
            f'{{"translated": "<translated sentence>"}}'
        )

        full_prompt = f"{prompt}\n\nTranslate this: {text}"
        response = model.generate_content(full_prompt)     
        raw_output = response.text.strip()

        match = re.search(r'\{.*\}', raw_output)
        if not match:
            raise ValueError("No JSON object found in the model response.")

        response_json = json.loads(match.group(0))
        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
