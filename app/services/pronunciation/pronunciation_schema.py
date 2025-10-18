from pydantic import BaseModel
from typing import List, Optional, Any

class pronunciation_request(BaseModel):
    words: str
    time_length: str
    language: str

class pronunciation_response(BaseModel):
    target_language: str
    english: str
    english_url: str
    target_language_url: str