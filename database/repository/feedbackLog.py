from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash

def feedbackInstance(request: schemas.feedback.DocumentLog, db: Session):
    log = models.FeedbackData(
        UserID=request.UserID,
        document_id=request.document_id,
        ocr_text=request.ocr_text,
        doc_type=request.doc_type,
        review=request.review,
        date=request.date
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    return log