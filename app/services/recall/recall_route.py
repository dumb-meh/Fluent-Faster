from fastapi import APIRouter,HTTPException,Body
from .recall import Recall
from .recall_schema import recall_response

router= APIRouter()
recall= Recall()

@router.post("/recall",response_model=recall_response)
async def get_recall(request_data: str = Body(..., media_type="text/plain")):
    try:
        response=recall.get_recall(request_data)
        return recall_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))