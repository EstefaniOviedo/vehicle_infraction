from pydantic import BaseModel, Field
from datetime import datetime


class InfractionCreate(BaseModel):
    patent_plate: str
    timestamp: str
    comments: str


class Infraction(BaseModel):
    id: str = Field(..., alias="_id")
    patent_plate: str
    timestamp: datetime
    comments: str

    class Config:
        allow_population_by_field_name = True


class ResponseInfraction(BaseModel):
    message: str
    data: Infraction
