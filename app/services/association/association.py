import os
import json
import openai
from dotenv import load_dotenv
from .association_schema import association_response

load_dotenv ()

class Association:
    def __init__(self):
        self.client=openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_association(self, input_data:str)->association_response:
        prompt=self.create_prompt()
        data=input_data
        response=self.get_openai_response (prompt,data)
        return response
    
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
                - Sound associations (rhymes, alliteration, similar sounds)
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
    
    def get_gemini_response (self, prompt:str, data:str)->str:
        completion =self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role":"system", "content": prompt},{"role":"user", "content": data}],
            temperature=0.7            
        )
        return completion.choices[0].message.content
    

