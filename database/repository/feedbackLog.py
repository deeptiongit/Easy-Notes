from sqlalchemy.orm import Session
from .. import models, schemas


def feedbackInstance(request: schemas.feedback.DocumentLog, db: Session):
    log = models.FeedbackData(
        UserID=request.UserID,
        ocr_text=request.ocr_text,
        doc_type=request.doc_type,
        review=request.review,
        date=request.date
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    return log