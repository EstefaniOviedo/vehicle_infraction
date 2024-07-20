from fastapi import HTTPException
from datetime import datetime
from src.shared.infrastructure.db.crud import (
    inset_item,
    get_item,
)
from src.shared.infrastructure.config import get_settings
from src.shared.utils import convert_to_datetime

SETTINGS = get_settings()

collection = "infraction"
collection_vehicle = "vehicle"


async def insert_infraction(data):
    try:
        data_dic = dict(data)
        filter = {"patent_plate": data_dic.get("patent_plate")}
        vehicle = await get_item(collection_vehicle, filter)
        if vehicle is None:
            raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

        timestamp = convert_to_datetime(data_dic.get("timestamp"))
        vehicle = {
            "patent_plate": data_dic.get("patent_plate"),
            "timestamp": timestamp,
            "comments": data_dic.get("comments"),
            "person_email": vehicle.get("person_email"),
            "person_id": vehicle.get("person_id"),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result_id = await inset_item(collection, vehicle)
        result = {
            "_id": result_id,
            **data_dic,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_infractions(email):
    filter = {"person_email": email}
    projection = {
        "patent_plate": 1,
        "timestamp": 1,
        "comments": 1,
        "_id": {"$toString": "$_id"},
    }
    result = await get_item(collection, filter, projection)
    return result
