from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.shared.application.routes import main_router
from src.shared.infrastructure.db.connection import close_connection, open_connection
from src.shared.infrastructure.config import get_settings

SETTINGS = get_settings()

app = FastAPI(title=SETTINGS.APP_NAME)

app.include_router(main_router)


def configure_middlewares():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_event_handlers():
    app.add_event_handler("startup", open_connection)
    app.add_event_handler("shutdown", close_connection)


def configure():
    configure_middlewares()
    configure_event_handlers()


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=SETTINGS.APP_PORT, host="127.0.0.1")
else:
    configure()
