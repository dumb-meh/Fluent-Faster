from fastapi import APIRouter,HTTPException,Body
from .pronounciation import Pronounciation
from .pronounciation_schema import pronounciation_response

router= APIRouter()
pronounciation= Pronounciation()

@router.post("/pronuncitation",response_model=pronounciation_response)
async def get_pronuncitation(request_data: str = Body(..., media_type="text/plain")):
    try:
        response=pronounciation.get_pronuncitation(request_data)
        return pronounciation_response (response=response)
    
    except Exception as e:
        raise HTTPException (status_code=500, detail=str(e))