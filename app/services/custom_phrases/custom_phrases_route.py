from fastapi import APIRouter,HTTPException,Body
from .custom_phrases import Phrases
from .custom_phrases_schema import custom_phrases_response,custom_phrases_request

router= APIRouter()
recall= Phrases()

@router.post("/phrases",response_model=custom_phrases_response)
async def create_phrases (request_data:custom_phrases_request):
    try:
        response=recall.get_recall(request_data)
        return custom_phrases_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))