import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .custom_phrases_schema import custom_phrases_response, custom_phrases_request

load_dotenv()

class Phrases:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def create_phrases(self, input_data: custom_phrases_request) -> custom_phrases_response:
        prompt = self.create_prompt(input_data)
        response = self.model.generate_content(prompt)
        print(response.text)
        try:
            text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {e}")
    
    def create_prompt(self, input_data: custom_phrases_request) -> str:
        return f"""
                You are an AI assistant that creates follow-up content for language learning. Based on the user's data, generate exactly {input_data.number_of_question} relevant, natural-sounding outputs. **You MUST return a valid JSON format as described below.**

                USER INFORMATION:
                - Topic: {input_data.topic}
                - User Details: {json.dumps(input_data.user_info)}


                IMPORTANT FORMAT RULE:
                If topic == "dialogue":
                - Return a JSON array of dictionaries (like a conversation)
                - Alternate between "user" and another speaker (e.g., "boss", "friend", etc.)
                - Each dict must have only one line of dialogue per speaker:
                Example:
                [
                    {{"user": "Hi, I wanted to talk about the project."}},
                    {{"boss": "Sure, what's going on?"}}
                ]

                Else:
                - Return a JSON array of strings:
                Example:
                [
                    "What exactly is blocking the project?",
                    "How have you approached this with your boss before?"
                ]

                INSTRUCTIONS:
                1. Generate exactly {input_data.number_of_question} follow-up outputs
                2. Keep it natural and contextually relevant
                3. Use the user-provided information to personalize your content
                4. DO NOT return anything outside the specified JSON format
                5. Do not include explanations, prefaces, or code
                6. DO NOT use placeholders like [Name], [Thing], [Technique]. Always use realistic, fully written examples.

                QUESTION STRATEGY:
                - Clarify or expand on the user’s responses
                - Ask about experiences, preferences, goals, or comparisons
                - Be conversational and realistic
                - For dialogue: simulate a natural back-and-forth interaction

                Begin generating based on the input above.
            """


    


