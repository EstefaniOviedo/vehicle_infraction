from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    patent_plate: str
    brand: str
    color: str
    person_email: str


class ResponseVehicle(BaseModel):
    id: str = Field(..., alias="_id")
    patent_plate: str
    brand: str
    color: str
    person_id: str
    person_email: str

    class Config:
        allow_population_by_field_name = True


class ReponseVehicleCreate(BaseModel):
    message: str
    data: ResponseVehicle
