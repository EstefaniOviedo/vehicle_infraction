from fastapi import APIRouter

main_router = APIRouter()

from src.user.application.user import router as user_router
from src.user.application.official import router as official_router
from src.user.application.person import router as person_router
from src.vehicle.application.vehicle import router as vehicle_router
from src.vehicle.application.infraction import router as infraction_router


# Root
@main_router.get("/")
def root():
    return {"message": "Hello World!"}


main_router.include_router(user_router)
main_router.include_router(official_router)
main_router.include_router(person_router)
main_router.include_router(vehicle_router)
main_router.include_router(infraction_router)
