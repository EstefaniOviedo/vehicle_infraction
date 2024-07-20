from fastapi import APIRouter, HTTPException, Security
from typing import Annotated

from src.vehicle.infrastructure.infraction import insert_infraction, get_infractions
from src.user.infrastructure.user import get_current_active_user
from src.user.domain.user_schema import User
from src.vehicle.domain.infraction_schema import InfractionCreate, ResponseInfraction


router = APIRouter()


@router.get("/generar_informe")
async def get_infraction(email: str) -> ResponseInfraction:
    try:
        data = await get_infractions(email)
        result = {
            "message": "Operación exitosa",
            "data": data,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cargar_infraccion")
async def create_infraction(
    infraction: InfractionCreate,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["cargar_infraccion"])
    ],
):
    try:
        dict_data = dict(infraction)
        data_insert = await insert_infraction(dict_data)
        result = {
            "message": "Infraccion creada exitosamente",
            "data": data_insert,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
