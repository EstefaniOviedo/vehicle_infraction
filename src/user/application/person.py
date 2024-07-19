from fastapi import APIRouter, HTTPException, Security
from typing import Annotated

from src.user.infrastructure.person import (
    get_people_inf,
    insert_person,
    update_person_inf,
    delete_person_inf,
)
from src.user.infrastructure.user import get_current_active_user
from src.user.domain.user_schema import User
from src.user.domain.person_schema import Person, ReponsePersonCreate


router = APIRouter()


@router.get("/people")
async def get_people(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["people"])],
):
    try:
        data = await get_people_inf()
        result = {
            "message": "Operación exitosa",
            "data": data,
        }
        print("Resul", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/person")
async def create_person(
    person: Person,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["person"])],
) -> ReponsePersonCreate:
    try:
        dict_person = dict(person)
        result_insert = await insert_person(dict_person)
        data = {
            "_id": str(result_insert),
            **dict_person,
        }
        result = {
            "message": "Registro creado exitosamente",
            "data": data,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/person/{_id}")
async def update_person(
    _id: str,
    person: Person,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["person"])],
) -> ReponsePersonCreate:
    try:
        response = await update_person_inf(_id, person)
        result = {
            "message": "Registro actualizado exitosamente",
            "data": response,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/person/{_id}")
async def delete_person(
    _id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["person"])],
):
    try:
        await delete_person_inf(_id)
        result = {
            "message": "Registro eliminado exitosamente",
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
