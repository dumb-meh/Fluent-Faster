import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from .custom_phrases import custom_phrases_response, custom_phrases_request

load_dotenv()

class Phrases:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def create_phrases (self, input_data=custom_phrases_request) -> custom_phrases_response:
        prompt = self.create_prompt()
        full_prompt = f"{prompt}\n\nInput: {input_data}"
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def create_prompt(self) -> str:
        return """ You are an expert language learning assistant that creates conversational phrases for practice. Based on the provided topic and user information, generate natural, practical phrases that learners can use in real conversations.

                    INSTRUCTIONS:
                    1. Generate phrases based on the topic provided
                    2. Use the user_info to personalize and contextualize the phrases
                    3. Create realistic, conversational language appropriate for the user's age and gender
                    4. Make phrases practical and commonly used in real-life situations
                    5. Vary sentence structures and complexity appropriately
                    6. Default to 4 phrases unless a specific number is mentioned in user_info

                    SPECIAL HANDLING FOR TOPICS:

                    **Dialogues Topic:**
                    - Create a full conversation between the user and the specified person
                    - Use the conversation context provided
                    - Generate the requested number of phrases (conversation turns)
                    - Alternate between the user and the other person
                    - Make it feel natural and realistic

                    **Other Topics (About Me, Work, Family, Hobbies, Travel, Love, Food, Custom):**
                    - Generate phrases the user would say when discussing this topic
                    - Make them personal based on the user's information
                    - Include both questions they might ask and statements they might make
                    - Focus on natural, conversational language

                    OUTPUT FORMAT:
                    Return a list of dictionaries where each dictionary contains:
                    - "phrase": The conversational phrase or statement
                    - "context": Brief explanation of when/how to use this phrase (optional for dialogues)

                    For Dialogues topic, use:
                    - "speaker": Either "user" or the other person's role
                    - "phrase": What that person says

                    EXAMPLES:

                    Topic: "Hobbies", User: 25-year-old male who plays guitar
                    Output: [
                    {"phrase": "I've been playing guitar for about 5 years now", "context": "When someone asks about your hobbies"},
                    {"phrase": "Do you play any instruments yourself?", "context": "To continue the conversation about music"},
                    {"phrase": "I usually practice in the evenings after work", "context": "When explaining your routine"},
                    {"phrase": "My favorite genre to play is probably rock or blues", "context": "When discussing musical preferences"}
                    ]

                    Topic: "Dialogues", Conversation with: mom, About: asking for money, 3 phrases, User: 20-year-old female
                    Output: [
                    {"speaker": "user", "phrase": "Mom, I was wondering if I could borrow some money for textbooks this semester?"},
                    {"speaker": "mom", "phrase": "How much do you need, and when can you pay me back?"},
                    {"speaker": "user", "phrase": "I need about $200, and I can pay you back from my part-time job by the end of the month"}
                    ]

                    Generate phrases that are:
                    - Natural and conversational
                    - Appropriate for the user's demographic
                    - Relevant to real-life situations
                    - Varied in structure and complexity
                    - Culturally appropriate and commonly used

                    Begin generating based on the provided topic and user_info."""
    


