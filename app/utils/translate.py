from fastapi import APIRouter, HTTPException, Form
import gemini
import os
from dotenv import load_dotenv
import json

router = APIRouter()
load_dotenv()

@router.post("/translate")
async def translate_text(
    text: str = Form(...),
    language: str = Form(...)
):
    try:
        client = gemini.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))

        prompt = (
            f"You are a translation assistant.\n"
            f"Translate the following sentence to {language}.\n"
            f"Return ONLY the translation in JSON format like this:\n"
            f'{{"translated": "<translated sentence>"}}'
        )

        content = f"Translate this: {text}"

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.5
        )
        response_text = completion.choices[0].message.content
        response_json = json.loads(response_text)

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))