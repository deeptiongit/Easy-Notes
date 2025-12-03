from pydantic import BaseModel

class Client(BaseModel):
    name:str
    email:str
    password:str

class ShowClient(BaseModel):
    name:str
    email:str
    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str