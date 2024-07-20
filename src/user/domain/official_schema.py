from pydantic import BaseModel, Field


class Official(BaseModel):
    email: str
    name: str
    password: str


class ResponseOfficial(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    official_key: str

    class Config:
        allow_population_by_field_name = True


class ResponseOfficialCreate(BaseModel):
    message: str
    data: ResponseOfficial
