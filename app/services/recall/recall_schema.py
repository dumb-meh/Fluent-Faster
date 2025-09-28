from pydantic import BaseModel
from typing import List

class recall_request(BaseModel):
    words: str
    language: str
    number_of_sentences: str
    user_id: str

class recall_response(BaseModel):
    target_language: str
    english: str