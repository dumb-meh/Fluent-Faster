from fastapi import APIRouter,HTTPException,Body
from .pronunciation import Pronunciation
from .pronunciation_schema import pronunciation_response,pronunciation_request

router= APIRouter()
pronunciation= Pronunciation()

@router.post("/pronunciation",response_model=pronunciation_response)
async def get_pronuncitation(request:pronunciation_request):
    try:
        response=pronunciation.get_pronunciation(request)
        return pronunciation_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))