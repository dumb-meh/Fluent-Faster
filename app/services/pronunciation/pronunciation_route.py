from fastapi import APIRouter,HTTPException
from typing import List
from .pronunciation import Pronunciation
from .pronunciation_schema import pronunciation_response,pronunciation_request

router= APIRouter()
pronunciation= Pronunciation()

@router.post("/pronunciation",response_model= List[pronunciation_response])
async def get_pronuncitation(request:pronunciation_request):
    try:
        response=pronunciation.get_pronunciation(request)
        return response
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))