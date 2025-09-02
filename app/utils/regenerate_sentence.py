from fastapi import APIRouter, HTTPException, Body
import json
import openai
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

@router.post("/regenerate_sentence")
async def regenerate_sentence(request_data: str = Body(..., media_type="text/plain")):
    try:
        client = openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))
        
        prompt = (
            "You will be given an English sentence and its translation in another language.\n"
            "Make the foreign sentence more advanced or complex, and give a new English translation for it.\n"
            "Return the result as a JSON object with two keys: 'english' and 'foreign'."
        )

        completion = client.chat.completions.create(
            model="gemini-2.5-flash", 
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": request_data}
            ],
            temperature=0.7
        )
        
        response_text = completion.choices[0].message.content
        response_json = json.loads(response_text)

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







