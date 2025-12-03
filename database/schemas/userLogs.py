from pydantic import BaseModel


class LogBase(BaseModel):
    title: str
    body: str

class Log(LogBase):
    class Config:
        orm_mode = True

class ShowLog(BaseModel):
    title: str
    body:str
    creator: ShowClient

    class Config:
        orm_mode = True