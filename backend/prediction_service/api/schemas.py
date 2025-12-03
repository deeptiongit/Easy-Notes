from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ForwardMessage(BaseModel):
    document_id: str
    ocr_text: str
    doc_type: str
    date: datetime = datetime.utcnow()
    curr_model_path: str

class BackwardMessage(BaseModel):
    document_id: str
    action: str  # e.g. "retrain" or "clear"
    curr_model_path: str
