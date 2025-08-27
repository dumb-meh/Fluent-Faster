from fastapi import APIRouter,HTTPException,Body
import os
import json
import openai
from dotenv import load_dotenv
router= APIRouter()
load_dotenv ()

@router.post("/utils/translate")
async def get_recall(request_data: str = Body(..., media_type="text/plain")):
    api_key=os.getenv("GEMINI_API_KEY")
    




class Pronunciation:
    def __init__(self):
        self.client=openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_pronunciation(self, input_data:str)->pronounciation_response:
        prompt=self.create_prompt()
        completion =self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role":"system", "content": prompt},{"role":"user", "content": data}],
            temperature=0.7            
        )
        return completion.choices[0].message.content
    

