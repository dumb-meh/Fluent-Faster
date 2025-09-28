from fastapi import APIRouter,HTTPException,Body
from .recall import Recall
from .recall_schema import recall_response,recall_request
from typing import List

router= APIRouter()
recall= Recall()

@router.post("/recall",response_model=List[recall_response])
async def get_recall(request_data:recall_request):
    try:
        response=recall.get_recall(request_data)
        return response
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))