from pydantic import BaseModel, Field


class Person(BaseModel):
    email: str
    name: str
    password: str


class ResponsePerson(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str

    class Config:
        allow_population_by_field_name = True


class ReponsePersonCreate(BaseModel):
    message: str
    data: ResponsePerson
