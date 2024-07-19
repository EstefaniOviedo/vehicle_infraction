from fastapi import APIRouter, HTTPException, Security
from typing import Annotated

from src.user.infrastructure.official import get_officials, insert_official, update_official_inf
from src.user.infrastructure.user import get_current_active_user
from src.user.domain.user_schema import User
from src.user.domain.official_schema import Official, ResponseOfficial


router = APIRouter()

@router.get("/official")
async def get_official(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ]
):
    try:
        data = get_officials()
        result = {
            "message": "Operación exitosa",
            "data": data,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/official")
async def create_official(official: Official, current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ])-> ResponseOfficial:
    try: 
        dict_official = dict(official)
        result_insert = await insert_official(dict_official)
        data = {
            "_id": str(result_insert),
            **dict_official,
        }
        result = {
            "message": "Registro creado exitosamente",
            "data": data,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.put("/official/{_id}")
async def update_official(_id: str, official: Official, current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ])-> ResponseOfficial:
    try:
        response = await update_official_inf(_id, official)
        result = {
            "message": "Registro actualizado exitosamente",
            "data": response,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.delete("/official/{_id}")
async def delete_official(_id: str, current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ]):
    try:
        await delete_official(_id)
        result = {
            "message": "Registro eliminado exitosamente",
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
