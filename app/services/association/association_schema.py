from pydantic import BaseModel
from typing import List, Optional, Any

class association_request(BaseModel):
    words: str

class association_response(BaseModel):
    mnemonic_association: str