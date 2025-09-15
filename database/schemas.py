from typing import List, Optional
from pydantic import BaseModel


class LogBase(BaseModel):
    title: str
    body: str

class Log(LogBase):
    class Config:
        orm_mode = True

class Client(BaseModel):
    name:str
    email:str
    password:str

class ShowClient(BaseModel):
    name:str
    email:str
    # blogs : List[Log] =[]
    class Config:
        orm_mode = True

class ShowLog(BaseModel):
    title: str
    body:str
    creator: ShowClient

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None