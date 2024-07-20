from pydantic import BaseModel
from typing import Union


class Login(BaseModel):
    email: str
    password: str


class ResponseLogin(BaseModel):
    token: str


class User(BaseModel):
    email: Union[str, None] = None
    active: Union[bool, None] = None
