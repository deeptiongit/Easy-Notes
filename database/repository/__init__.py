"""
Repository layer for database operations
"""
from sqlalchemy.orm import Session
from .. import models
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def save_feedback(
    db: Session,
    document_id: str,
    ocr_text: str,
    doc_type: str,
    date: str
) -> bool:
    """
    Save feedback data to database
    
    Args:
        db: Database session
        document_id: Document identifier
        ocr_text: Extracted text
        doc_type: Type of document
        date: Date of feedback
        
    Returns:
        True if successful
    """
    try:
        feedback = models.FeedbackData(
            document_id=document_id,
            ocr_text=ocr_text,
            doc_type=doc_type,
            date=date
        )
        db.add(feedback)
        db.commit()
        logger.info(f"Saved feedback for document {document_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save feedback: {str(e)}")
        return False

def clear_feedback(db: Session, document_id: Optional[str] = None) -> bool:
    """
    Clear feedback data from database
    
    Args:
        db: Database session
        document_id: Optional specific document ID to clear
        
    Returns:
        True if successful
    """
    try:
        if document_id:
            db.query(models.FeedbackData).filter(
                models.FeedbackData.document_id == document_id
            ).delete()
        else:
            db.query(models.FeedbackData).delete()
        
        db.commit()
        logger.info(f"Cleared feedback data")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clear feedback: {str(e)}")
        return False