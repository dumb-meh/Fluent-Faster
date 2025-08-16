from pydantic import BaseModel
from typing import List, Optional, Any

class pronounciation_request(BaseModel):
    words: str
    time_length:str
    language:str

class pronounciation_response(BaseModel):
    create_sentence: List[Any]