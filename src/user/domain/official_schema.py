from pydantic import BaseModel

class Official(BaseModel):
    name: str
    official_key: str
    password: str
    
class ResponseOfficial(BaseModel):
    _id: str
    name: str
    official_key: str
