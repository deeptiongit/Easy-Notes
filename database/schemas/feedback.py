from pydantic import BaseModel
from datetime import datetime


class FeedbackData(BaseModel):
    UserID: str

class DocumentLog(FeedbackData):
    UserID :int
    document_id :str
    ocr_text :str
    doc_type :str
    review:str
    date :datetime

    class Config:
        orm_mode = True