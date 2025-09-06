import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .shadowing_schema import shadowing_response, shadowing_request

load_dotenv()

class Shadowing:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def get_shadowing(self, input_data: str) -> str:
        prompt = self.create_prompt()
        full_prompt = f"{prompt}\n\nInput: {input_data}"
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def create_prompt(self) -> str:
        return """You are a language learning assistant that creates shadowing practice sentences. Your task is to generate sentences optimized for shadowing technique - where learners listen to and simultaneously repeat target language sentences to improve pronunciation, rhythm, and fluency.

                INPUT:
                - words: English words (as a string)
                - language: Target language for sentence creation
                - number_of_sentences: Exact number of sentences to create (e.g., "5", "8", "12")

                OUTPUT: A list of sentence pairs in the target language that:
                1. Incorporate ALL the provided English words naturally across the sentences
                2. Are grammatically correct in the target language
                3. Match the exact number of sentences requested
                4. Are specifically optimized for shadowing practice
                5. Include both the target language sentence AND its English translation for comprehension

                SHADOWING OPTIMIZATION RULES:
                1. Create sentences with natural speech rhythm and flow
                2. Use conversational, everyday language patterns
                3. Include varied intonation patterns (statements, questions, exclamations)
                4. Incorporate common collocations and phrases native speakers use
                5. Design sentences that flow smoothly when spoken aloud
                6. Include appropriate pauses and breathing points for longer sentences
                7. Use realistic speech tempo and natural word stress patterns

                SENTENCE CHARACTERISTICS FOR SHADOWING:
                - Natural conversational style (avoid overly formal or academic language)
                - Clear pronunciation targets (words that practice specific sounds)
                - Varied sentence lengths (mix short punchy sentences with longer flowing ones)
                - Emotional expression to practice intonation
                - Common sentence patterns native speakers use frequently
                - Progressive difficulty if multiple sentences (start easier, build complexity)

                LANGUAGE-SPECIFIC CONSIDERATIONS:
                - Emphasize target language's natural rhythm and stress patterns
                - Include language-specific pronunciation challenges
                - Use authentic expressions and idioms when appropriate
                - Consider syllable timing vs. stress timing languages
                - Incorporate natural liaison and connected speech patterns
                - Adapt to target language's typical intonation contours

                SPEECH FLOW OPTIMIZATION:
                - Ensure smooth transitions between words
                - Include natural pausing points
                - Create sentences that encourage proper breathing
                - Use words that flow well together phonetically
                - Avoid tongue-twisters unless specifically targeting difficult sounds
                - Design for comfortable speaking pace

                QUALITY CHECKS:
                - Verify all English words are used appropriately
                - Confirm exact sentence count matches request
                - Test sentences for natural speech flow when read aloud
                - Ensure authentic conversational tone
                - Check for appropriate shadowing difficulty level

                EXAMPLE OUTPUT FORMAT:
                [
                    {"target_language": "Sentence 1 in target language", "english": "Sentence 1 in English"},
                    {"target_language": "Sentence 2 in target language", "english": "Sentence 2 in English"},
                    {"target_language": "Sentence 3 in target language", "english": "Sentence 3 in English"}
                ]

                Now generate shadowing practice sentences that will help learners develop natural pronunciation, rhythm, and fluency in the target language."""


