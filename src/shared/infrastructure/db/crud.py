from src.shared.infrastructure.db.connection import db
from bson import ObjectId
from src.shared.infrastructure.config import get_settings

SETTINGS = get_settings()


def get_database():
    database_name = SETTINGS.MONGODB_DB_NAME
    database = db.client[database_name]
    return database


async def inset_item(collection_name, item):
    database = get_database()
    collection = database[collection_name]
    result = await collection.insert_one(item)
    return str(result.inserted_id)


async def get_items(
    collection_name, filters=None, projection=None, sort=None, limit=None, skip=None
):
    """Get all the records of a collection"""
    database = get_database()
    collection = database[collection_name]
    result = collection.find(
        filters or {}, projection=projection or None, sort=sort or None
    )
    if skip is not None:
        result = result.skip(skip)
    if limit is not None:
        result = result.limit(limit)

    result = await result.to_list(length=None)
    return result


async def update(collection_name, item, _id):
    database = get_database()
    collection = database[collection_name]
    result = await collection.update_one(
        {"_id": ObjectId(_id)}, {"$set": item}, upsert=False
    )
    return result.modified_count


async def get_item(collection_name, filters=None, projection=None):
    """Get record of a collection"""
    database = get_database()
    collection = database[collection_name]
    result = await collection.find_one(
        filters or {},
        projection=projection or None,
    )
    return result


async def get_item_id(collection_name, _id):
    """Get record of a collection"""
    database = get_database()
    collection = database[collection_name]
    result = await collection.find_one(
        {"_id": ObjectId(_id)},
    )
    return result
