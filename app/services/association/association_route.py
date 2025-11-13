from fastapi import APIRouter,HTTPException,Body
from .association import Association
from .association_schema import association_response

router= APIRouter()
association= Association()

@router.post("/association",response_model=association_response)
async def get_association(request_data: str = Body(..., media_type="text/plain")):
    try:
        response=association.get_association(request_data)
        return association_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))