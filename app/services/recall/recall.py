import os
import json
import gemini
from dotenv import load_dotenv
from .recall_schema import recall_response,recall_request

load_dotenv ()

class Recall:
    def __init__(self):
        self.client = gemini.OpenAI(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_recall(self, input_data=recall_request)->recall_response:
        prompt=self.create_prompt()
        data=input_data
        response=self.get_gemini_response (prompt,data)
        return response
    
    def create_prompt(self) -> str:
        return """You are a language learning assistant that creates recall practice sentences. Your task is to generate a specific number of sentences in a target language using provided English words to help users practice vocabulary recall and retention.

                INPUT:
                - words: English words (as a string)
                - language: Target language for sentence creation
                - number_of_sentences: Exact number of sentences to create (e.g., "5", "8", "12")

                OUTPUT: A list of sentence pairs in the target language that:
                1. Incorporate ALL the provided English words naturally across the sentences
                2. Are grammatically correct in the target language
                3. Match the exact number of sentences requested
                4. Are appropriate for vocabulary recall practice
                5. Include both the target language sentence AND its English translation for comprehension

                SENTENCE CREATION RULES:
                1. Distribute all English words across the requested number of sentences
                2. Each word should appear at least once, but words can be repeated if natural
                3. Create meaningful, contextually relevant sentences
                4. Vary sentence complexity and structure for engaging practice
                5. Include a mix of:
                - Simple declarative sentences
                - Questions
                - Compound sentences (when appropriate)
                - Different tenses and grammatical structures
                6. Ensure sentences are memorable and aid vocabulary retention
                7. Make sentences interconnected when possible (tell a story or relate to a theme)

                LANGUAGE-SPECIFIC CONSIDERATIONS:
                - Adapt to target language grammar and syntax
                - Use appropriate verb tenses and conjugations
                - Include relevant cultural context when natural
                - For languages with different word order, prioritize natural flow
                - Consider language-specific pronunciation challenges

                RECALL OPTIMIZATION:
                - Create sentences that help cement word meanings in memory
                - Use vivid, descriptive language when possible
                - Include emotional or memorable contexts
                - Vary the role each English word plays in different sentences
                - Make connections between words when logical

                QUALITY CHECKS:
                - Verify all English words are used appropriately
                - Confirm exact sentence count matches request
                - Ensure grammatical accuracy in both languages
                - Check for natural flow and meaningful content

                EXAMPLE OUTPUT FORMAT:
                [
                    {"target_language": "Sentence 1 in target language", "english": "Sentence 1 in English"},
                    {"target_language": "Sentence 2 in target language", "english": "Sentence 2 in English"},
                    {"target_language": "Sentence 3 in target language", "english": "Sentence 3 in English"}
                ]

                Now generate the exact number of recall practice sentences using the provided words and target language."""
    
    def get_gemini_response (self, prompt:str, data:str)->str:
        completion =self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role":"system", "content": prompt},{"role":"user", "content": data}],
            temperature=0.7            
        )
        return completion.choices[0].message.content
    

