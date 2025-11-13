from fastapi import APIRouter, HTTPException, Body
from .shadowing import Shadowing
from .shadowing_schema import shadowing_response,shadowing_request
from typing import List

router = APIRouter()
shadowing = Shadowing()

@router.post("/shadowing", response_model=List[shadowing_response])
async def get_shadowing(request_data:shadowing_request):
    try:
        response = shadowing.get_shadowing(request_data)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))