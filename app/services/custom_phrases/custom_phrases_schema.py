from pydantic import BaseModel
from typing import List, Union

class custom_phrases_request(BaseModel):
    topic:str
    user_info:List[dict[str,str]]
    number_of_question: int

class custom_phrases_response(BaseModel):
    response: Union[List[dict[str, str]], List[str]]