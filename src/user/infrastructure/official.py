import uuid
from fastapi import HTTPException
from datetime import datetime
from src.shared.infrastructure.db.crud import (
    get_items,
    inset_item,
    update,
    get_item_id,
)
from src.shared.infrastructure.config import get_settings
from src.user.infrastructure.user import get_password_hash

SETTINGS = get_settings()

collection = "users"


async def generate_employee_id():
    # Pref for ids
    prefix = "EMP"

    # date format YYYYMMDDHHMMSS
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # UUID4 for generate idenntifier random unique
    unique_suffix = uuid.uuid4().hex[:6]

    employee_id = f"{prefix}{now}{unique_suffix}"

    return employee_id


async def get_officials():
    filter = {"type": "oficial", "active": True}
    projection = {"_id": 1, "name": 1, "official_key": 1}
    result = await get_items(collection, filter, projection)

    for item in result:
        item["_id"] = str(item.get("_id"))
    return result


async def insert_official(data):
    try:
        new_official_id = await generate_employee_id()
        password = await get_password_hash(data.get("password"))
        official = {
            "name": data.get("name"),
            "email": data.get("email"),
            "official_key": new_official_id,
            "password": password,
            "active": True,
            "type": "oficial",
            "scopes": ["oficial"],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result_id = await inset_item(collection, official)
        official_respon = {
            "name": data.get("name"),
            "official_key": new_official_id,
        }
        result = {
            "_id": result_id,
            **official_respon,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_official_inf(_id, data):
    official_dic = dict(data)
    find_off = await get_item_id(collection, _id)
    if find_off is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    official_dic["updated_at"] = datetime.now()
    await update(collection, official_dic, _id)
    official_respon = {
        "name": official_dic.get("name"),
        "email": official_dic.get("email"),
    }
    result = {
        "_id": _id,
        **official_respon,
    }
    return result


async def delete_official_inf(_id):
    find_official = await get_item_id(collection, _id)
    if find_official is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    official_dic = {"active": False}
    result = await update(collection, official_dic, _id)
    return result
