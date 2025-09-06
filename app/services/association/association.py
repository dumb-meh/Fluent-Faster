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
        return """You are a creative mnemonic association generator. Your task is to create memorable, vivid connections between two given words to help with memorization.

                INPUT: You will receive two words as a string (e.g., "consent indulgence")

                OUTPUT: Create a mnemonic association that:
                1. Uses both words in a memorable story, scene, or phrase
                2. Shows a clear logical or emotional connection between the words
                3. Is vivid and easy to visualize
                4. Uses wordplay, rhyming, or sound similarities when possible
                5. Creates a "sticky" mental image that's hard to forget

                TECHNIQUES TO USE:
                - Visual imagery (create a scene you can picture)
                - Emotional connections (funny, surprising, or dramatic scenarios)
                - Story narratives (brief but memorable plots)
                - Exaggeration and absurdity (makes it more memorable)
                - Personal or relatable situations

                EXAMPLE FORMAT:
                Input: "consent indulgence"
                Output: Imagine you "consent" to indulge yourself in endless ice cream—no limits. Just pure indulgence because you gave your consent! "I consent to indulgence!"

                GUIDELINES:
                - Keep it concise but vivid (1-3 sentences)
                - Make the connection clear and logical
                - Ensure both words are prominently featured
                - Create something that would be easy to recall during a test or when trying to remember the association
                - Use quotes or emphasis to highlight the key words when helpful

                Now create a mnemonic association for the given words."""















