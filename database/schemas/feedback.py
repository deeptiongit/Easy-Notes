from pydantic import BaseModel
from datetime import datetime


class FeedbackData(BaseModel):
    UserID: str

class DocumentLog(FeedbackData):
    UserID :str
    ocr_text :str
    doc_type :str
    review:str
    date :datetime

    class Config:
        orm_mode = True

