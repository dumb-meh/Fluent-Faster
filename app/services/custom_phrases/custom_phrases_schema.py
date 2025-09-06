from pydantic import BaseModel
from typing import List

class custom_phrases_request(BaseModel):
    topic:str
    user_info:List[dict[str,str]]

class custom_phrases_response(BaseModel):
    response:  List[dict[str,str]]