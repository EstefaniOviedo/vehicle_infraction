"""Module for load system variables"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Class to define variables"""

    APP_NAME: str = "Base API"
    APP_ENVIRONMENT: str = "dev"
    APP_LOGGING_LEVEL: str = "INFO"
    APP_PORT: int = 3000
    MONGODB_URI: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "admin"
    MONGODB_MAX_CONNECTIONS: int = 10
    MONGODB_MIN_CONNECTIONS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM: str = ""
    SECRET_KEY: str = ""

    class Config:
        """Class to load variables file"""

        env_file = "../../.env"


@lru_cache()
def get_settings():
    return Settings()
