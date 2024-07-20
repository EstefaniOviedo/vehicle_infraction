from fastapi import APIRouter, HTTPException, Security
from typing import Annotated

from src.vehicle.infrastructure.vehicle import (
    get_vehicles,
    insert_vehicle,
    update_vehicle_inf,
    delete_vehicle_inf,
)
from src.user.infrastructure.user import get_current_active_user
from src.user.domain.user_schema import User
from src.vehicle.domain.vehicle_schema import Vehicle, ReponseVehicleCreate


router = APIRouter()


@router.get("/vehicle")
async def get_vehicle(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["vehicle"])
    ],
):
    try:
        data = await get_vehicles()
        result = {
            "message": "Operación exitosa",
            "data": data,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vehicle")
async def create_vehicle(
    vehicle: Vehicle,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["vehicle"])
    ],
) -> ReponseVehicleCreate:
    try:
        dict_vehicle = dict(vehicle)
        data_insert = await insert_vehicle(dict_vehicle)
        result = {
            "message": "Registro creado exitosamente",
            "data": data_insert,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/vehicle/{_id}")
async def update_vehicle(
    _id: str,
    vehicle: Vehicle,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["vehicle"])
    ],
) -> ReponseVehicleCreate:
    try:
        response = await update_vehicle_inf(_id, vehicle)
        result = {
            "message": "Registro actualizado exitosamente",
            "data": response,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/vehicle/{_id}")
async def delete_vehicle(
    _id: str,
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["vehicle"])
    ],
):
    try:
        await delete_vehicle_inf(_id)
        result = {
            "message": "Registro eliminado exitosamente",
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
