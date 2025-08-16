from pydantic import BaseModel
from typing import List, Optional, Any

class pronuncitation_request(BaseModel):
    words: str
    time_length:str
    language:str

class pronuncitation_response(BaseModel):
    create_sentence: List[Any]