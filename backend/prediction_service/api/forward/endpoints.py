from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas import ForwardMessage
from ...core import predictor
from database import repository, database

router = APIRouter()

@router.post("/forward")
def forward_message(msg: ForwardMessage, db: Session = Depends(database.get_db)):
    try:
        # Try model prediction
        prediction = predictor.predict(msg.ocr_text, model_path=msg.curr_model_path)
        
        if prediction["status"] == "failed" or prediction.get("feedback") == "negative":
            # Save to feedback DB
            repository.save_feedback(
                db=db,
                document_id=msg.document_id,
                ocr_text=msg.ocr_text,
                doc_type=msg.doc_type,
                date=str(msg.date)
            )
            
            # Run fallback LLM
            fallback_output = predictor.fallback_llm(msg.ocr_text)
            
            # Save current model snapshot
            predictor.save_curr_model(msg.curr_model_path)
            
            return {"status": "fallback_used", "output": fallback_output}
        
        return {"status": "success", "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))