from fastapi import APIRouter,HTTPException,Body
from .association import Association
from .association_schema import association_response

router= APIRouter()
story= Association()

@router.post("/pronuncitation",response_model=association_response)
async def get_pronuncitation(request_data: str = Body(..., media_type="text/plain")):
    try:
        response=story.get_pronuncitation(request_data)
        return association_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))