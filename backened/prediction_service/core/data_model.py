from pydantic import BaseModel

class FailureLog(BaseModel):
    doc_id: str
    error_type: str
    doc_type: str
    missing_field: str
    context: str
    payload: dict


class Feedback(BaseModel):
    doc_id: str
    decision: str
    correction: dict = {}
