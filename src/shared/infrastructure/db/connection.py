from motor.motor_asyncio import AsyncIOMotorClient

from src.shared.infrastructure.config import get_settings


SETTINGS = get_settings()


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_connection() -> AsyncIOMotorClient:
    return db.client


async def open_connection():
    """Create a mongo client"""
    
    db.client = AsyncIOMotorClient(
        SETTINGS.MONGODB_URI,
        maxPoolSize=SETTINGS.MONGODB_MAX_CONNECTIONS,
        minPoolSize=SETTINGS.MONGODB_MIN_CONNECTIONS,
    )
    print("Connected!")
    return db


async def close_connection():
    """Terminate mongo client"""
    print("Closing mongoDB connection...")
    db.client.close()
    print("Connection closed!")
    return db
