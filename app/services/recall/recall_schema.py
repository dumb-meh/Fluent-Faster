from pydantic import BaseModel
from typing import List

class recall_request(BaseModel):
    words: str
    language: str
    number_of_sentences: str

class recall_response(BaseModel):
    target_language: str
    english: str
    english_url: str
    target_language_url: str