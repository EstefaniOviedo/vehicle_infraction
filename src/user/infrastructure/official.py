import uuid
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId
from src.shared.infrastructure.db.crud import get_items, inset_item, update, get_item
from src.shared.infrastructure.config import get_settings
from src.user.infrastructure.user import get_password_hash

SETTINGS = get_settings()

collection = "users"

async def generate_employee_id():
    #Pref for ids
    prefix = "EMP"
    
    # date format YYYYMMDDHHMMSS
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # UUID4 for generate idenntifier random unique
    unique_suffix = uuid.uuid4().hex[:6]
    

    employee_id = f"{prefix}{now}{unique_suffix}"
    
    return employee_id

async def get_officials():
    result = get_items(collection)
    return result

async def insert_official(data):
    try: 
        new_official_id = await generate_employee_id()
        password = get_password_hash(data.get("password"))
        official = {
            "fullname": data.get("name"),
            "official_key": new_official_id,
            "password": password,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "type": "oficial",
        }
        result = inset_item(collection, official)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_official_inf(_id, data):
    find_official = get_item(collection, { "_id", ObjectId(_id)})
    if find_official is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    official_dic = dict(data)
    response = {
        "_id": _id,
        **official_dic
    }
    update(collection, official_dic,_id)
    return response

async def delete_official_inf(_id, data):
    find_official = get_item(collection, { "_id", ObjectId(_id)})
    if find_official is None:
        raise HTTPException(status_code=404, detail="Oficial no encontrado")
    official_dic = {
        "active": False
    }
    update(collection, official_dic,_id)
    