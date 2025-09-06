from pydantic import BaseModel
from typing import List, Optional, Any

class recall_request(BaseModel):
    words: str
    language: str
    number_of_sentences: str

class recall_response(BaseModel):
    response: str  