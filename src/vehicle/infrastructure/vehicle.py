from fastapi import HTTPException
from datetime import datetime
from src.shared.infrastructure.db.crud import (
    get_items,
    inset_item,
    update,
    get_item_id,
    get_item,
)
from src.shared.infrastructure.config import get_settings

SETTINGS = get_settings()

collection = "vehicle"
collection_user = "users"


async def get_vehicles():
    result = await get_items(collection, {"active": True})

    for item in result:
        item["_id"] = str(item.get("_id"))
    return result


async def insert_vehicle(data):
    try:
        data_dic = dict(data)

        filter = {"email": data_dic.get("person_email"), "type": "persona"}
        person_id = await get_item(collection_user, filter)
        if person_id is None:
            raise HTTPException(status_code=404, detail="Automovilista no encontrado")
        vehicle = {
            "patent_plate": data_dic.get("patent_plate"),
            "brand": data_dic.get("brand"),
            "color": data_dic.get("color"),
            "person_id": str(person_id.get("_id")),
            "person_email": data_dic.get("person_email"),
            "active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result_id = await inset_item(collection, vehicle)
        vehicle_respon = {
            "patent_plate": data_dic.get("patent_plate"),
            "brand": data_dic.get("brand"),
            "color": data_dic.get("color"),
            "person_id": str(person_id.get("_id")),
            "person_email": data_dic.get("person_email"),
        }
        result = {
            "_id": result_id,
            **vehicle_respon,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_vehicle_inf(_id, data):
    data_dic = dict(data)
    filter = {"email": data_dic.get("person_email"), "type": "persona"}
    person_id = await get_item(collection_user, filter)
    if person_id is None:
        raise HTTPException(status_code=404, detail="Automovilista no encontrado")
    data_dic["updated_at"] = datetime.now()
    await update(collection, data_dic, _id)
    vehicle_respon = {
        "patent_plate": data_dic.get("patent_plate"),
        "brand": data_dic.get("brand"),
        "color": data_dic.get("color"),
        "person_id": str(person_id.get("_id")),
        "person_email": data_dic.get("person_email"),
    }
    result = {
        "_id": _id,
        **vehicle_respon,
    }
    return result


async def delete_vehicle_inf(_id):
    find_vehicle = await get_item_id(collection, _id)
    if find_vehicle is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    vehicle_dic = {"active": False}
    result = await update(collection, vehicle_dic, _id)
    return result
