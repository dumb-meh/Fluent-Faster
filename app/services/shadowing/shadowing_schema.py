from pydantic import BaseModel
from typing import List, Optional, Any

class shadowing_request(BaseModel):
    words: str
    language: str
    number_of_sentences: str

class shadowing_response(BaseModel):
    target_language: str
    english: str
    english_url: str
    target_language_url: str

