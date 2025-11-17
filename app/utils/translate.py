from fastapi import APIRouter, HTTPException, Body
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

router = APIRouter()
load_dotenv()

@router.post("/translate")
async def translate_text(
    text: str = Body(...),
    base_language: str = Body(...),
    language: str = Body(...)
):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = (
            f"You are a translation assistant.\n"
            f"Translate the following sentence from {base_language} to {language}.\n"
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
    
    
    
@router.post("/word_translation")
async def translate_text(
    text: str = Body(...),
    base_language: str = Body(...),
    target_language: str = Body(...)
):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = f"""You are a language learning assistant that creates practice sentences. Your task is to generate 5 sentences in the base language using provided words to help users practice vocabulary.

                Here are some examples:

                EXAMPLE 1:
                Input: words="cat, happy, running", base_language="English", target_language="Spanish"
                Output: {{"words": "cat, happy, running", "translated_words": "gato, feliz, corriendo", "sentences": ["The cat is running in the garden.", "My cat looks very happy today.", "The happy cat is running towards me.", "Why is the cat running so happily?", "The running cat seems to be happy and healthy."]}}

                EXAMPLE 2:
                Input: words="book, read, library", base_language="English", target_language="French"
                Output: {{"words": "book, read, library", "translated_words": "livre, lire, bibliothèque", "sentences": ["I will read a book at the library.", "This book from the library is fascinating to read.", "Where can I read this new book in the library?", "The library has many books to read.", "She likes to read old books at the library."]}}

                EXAMPLE 3:
                Input: words="water, drink, cold", base_language="English", target_language="German"
                Output: {{"words": "water, drink, cold", "translated_words": "Wasser, trinken, kalt", "sentences": ["I like to drink cold water.", "The water is too cold to drink.", "Would you like to drink cold water?", "Drinking cold water is refreshing.", "He drinks cold water every morning."]}}

                INSTRUCTIONS:
                1. Incorporate ALL provided words naturally across 5 sentences
                2. Create grammatically correct sentences in the base language
                3. Vary sentence complexity (simple, questions, compound structures)
                4. Make sentences meaningful and contextually relevant
                5. Distribute words across sentences (each word at least once)
                6. Ensure sentences aid vocabulary retention

                Return only the JSON in this exact format:
                {{"words": "words that were provided", "translated_words": "words translated to target language", "sentences": ["sentence 1", "sentence 2", "sentence 3", "sentence 4", "sentence 5"]}}
                Now, generate 5 practice sentences using these words:
                Input: words="{text}", base_language="{base_language}", target_language="{target_language}"""

        response = model.generate_content(prompt)     
        raw_output = response.text.strip()

        match = re.search(r'\{.*\}', raw_output)
        if not match:
            raise ValueError("No JSON object found in the model response.")

        response_json = json.loads(match.group(0))
        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

