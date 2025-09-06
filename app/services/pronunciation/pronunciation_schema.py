from pydantic import BaseModel
from typing import List, Optional, Any

class pronunciation_request(BaseModel):
    words: str
    time_length: str
    language: str

class pronunciation_response(BaseModel):
    response: str 