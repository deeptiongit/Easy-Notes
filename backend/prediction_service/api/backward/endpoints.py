from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas import BackwardMessage
from ...core import trainer, predictor
from database import repository, database

router = APIRouter()

@router.post("/backward")
def backward_message(msg: BackwardMessage, db: Session = Depends(database.get_db)):
    try:
        if msg.action == "retrain":
            trainer.continuous_train(msg.curr_model_path)
            repository.clear_feedback(db, msg.document_id)
            predictor.update_nlp_extractor(msg.curr_model_path)
            return {"status": "model_updated"}
        
        elif msg.action == "clear":
            repository.clear_feedback(db, msg.document_id)
            return {"status": "feedback_cleared"}
        
        else:
            return {"status": "invalid_action"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))