from fastapi import HTTPException
from datetime import datetime
from src.shared.infrastructure.db.crud import get_items, inset_item, update, get_item_id
from src.shared.infrastructure.config import get_settings
from src.user.infrastructure.user import get_password_hash

SETTINGS = get_settings()

collection = "users"


async def get_people_inf():
    filter = {"type": "persona", "active": True}
    projection = {"_id": 1, "name": 1, "email": 1}
    result = await get_items(collection, filter, projection)

    for item in result:
        item["_id"] = str(item.get("_id"))

    return result


async def insert_person(data):
    try:
        password = await get_password_hash(data.get("password"))
        person = {
            "name": data.get("name"),
            "email": data.get("email"),
            "password": password,
            "active": True,
            "type": "person",
            "scopes": ["person"],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result_id = await inset_item(collection, person)
        person_respon = {
            "name": data.get("name"),
            "email": data.get("email"),
        }
        result = {
            "_id": result_id,
            **person_respon,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_person_inf(_id, data):
    person_dic = dict(data)
    find_off = await get_item_id(collection, _id)
    if find_off is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    person_dic["updated_at"] = datetime.now()
    await update(collection, person_dic, _id)
    person_respon = {
        "name": person_dic.get("name"),
        "email": person_dic.get("email"),
    }
    result = {
        "_id": _id,
        **person_respon,
    }
    return result


async def delete_person_inf(_id):
    find_person = await get_item_id(collection, _id)
    if find_person is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    person_dic = {"active": False}
    result = await update(collection, person_dic, _id)
    return result
