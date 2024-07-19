from fastapi import APIRouter

main_router = APIRouter()

from src.user.application.user import router as user_router
from src.user.application.official import router as official_router


# Root
@main_router.get("/")
def root():
    return {"message": "Hello World!"}

main_router.include_router(user_router)
main_router.include_router(official_router)
