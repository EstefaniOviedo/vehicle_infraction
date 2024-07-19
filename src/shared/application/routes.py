from fastapi import APIRouter

main_router = APIRouter()

from src.user.application.official import router as official_router  # noqa: E402

# Root
@main_router.get("/")
def root():
    return {"message": "Hello World!"}

main_router.include_router(official_router)
