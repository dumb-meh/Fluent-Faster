from pydantic import BaseModel
from typing import List, Optional, Any
class shadowing_request(BaseModel):
    words: str
    language:str
    number_of_sentences: str
class shadowing_response(BaseModel):
    create_sentence: List[Any]