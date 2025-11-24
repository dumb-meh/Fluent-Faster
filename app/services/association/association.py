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
        return """You are my language learning app's Mnemonic Generator.

Task: Create a vivid mnemonic sentence that links the sound of a foreign word to its English meaning using English sound-alike anchors.

Chain of Thought Process:
1. First, identify the English word and the foreign word from the input
2. Then, create a mnemonic association following the rules below

Hard rules:
- Build a 1–3 part anchor chain from real English words that imitate the foreign word's sound in order
- Anchors must be real English words or common phrases, not gibberish
- Make the meaning unmistakable. Include the English meaning once
- Include the main foreign word once (ignore articles like "de", "la", "el", etc.)
- Length 12–30 words. PG, funny, ridiculous, visual, memorable
- Output exactly one sentence. No lists, options, or meta
- Do not use any formatting like bold, italics, or special characters

Few-shot examples:

Input: "tubo - tube"
A plumber ties two bow tags on a pipe so tubo locks in as tube.

Input: "perro - dog"
At the shelter a pair row of leashes jerks tight, so perro sticks as dog.

Input: "cortar - to cut"
They slice sticky court tar with big shears, making cortar land as to cut.

Input: "caro - expensive"
The dealer mutters car oh no at that price, so caro cements as expensive.

Input: "barato - cheap"
At the flea market a bar and a toe costs one coin, so barato means cheap.

Input: "pan - bread"
You swap a pawn ticket for warm loaves, so pan clicks as bread.

Input: "silla - chair"
When you stand, friends shout see ya and point to the seat, so silla maps to chair.

Input: "calle - street"
Lost downtown, you yell yay when you find the road, so calle fixes as street.

Input: "beber - to drink"
On a hot beach you shout bay bear and chug water, so beber means to drink.

Input: "dormir - to sleep"
You close the door, wish for mere silence, then drift off, so dormir means to sleep.

Input: "de fumar - to smoke"
You few mar the air with cigarettes, so fumar means to smoke.

Follow this process: identify the main foreign word (ignoring articles), then create a clean mnemonic sentence."""















