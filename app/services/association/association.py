import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Association:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def get_association(self, input_data: str) -> str:
        prompt = self.create_prompt()
        full_prompt = f"{prompt}\n\nInput: {input_data}"
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def create_prompt(self) -> str:
        return """generate a short and unforgettable mnemonic story/association (2-3 sentences max) that links the sound of the target word to its meaning. The mnemonic must use [base language] words or phrases that sound similar to the target word (phonetic link). The association must make the meaning obvious and memorable. Keep it funny, emotional, surprising, or visual — strong emotion boosts memory"""















