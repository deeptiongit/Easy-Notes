from fastapi import APIRouter, Request, BackgroundTasks
import redis, pickle, json, logging, os
import requests
import numpy as np
from . import integration as bi
from ..core import data_model as db

router = APIRouter()

@router.post("/log_failure")
def log_failure(failure: db.FailureLog):
    try:
        bi.r.rpush(bi.data_key, pickle.dumps(failure.model_dump()))
        bi.logger.info(f"Failure logged for doc_id={failure.doc_id}")
        return {"status": "logged"}
    except Exception as e:
        bi.logger.error(f"Log failure error: {str(e)}")
        return {"error": str(e)}


@router.post("/feedback")
def receive_feedback(feedback: db.Feedback):
    try:
        bi.r.rpush(bi.feedback_key, pickle.dumps(feedback.model_dump()))
        bi.logger.info(f"Feedback received for doc_id={feedback.doc_id}")
        return {"status": "feedback logged"}
    except Exception as e:
        bi.logger.error(f"Feedback error: {str(e)}")
        return {"error": str(e)}


@router.post("/predict_and_resolve")
def resolve(background_tasks: BackgroundTasks):
    try:
        model_bytes = bi.r.get(bi.model_key)
        if not model_bytes:
            bi.logger.warning("No model found.")
            return {"error": "Model not trained yet."}

        model = pickle.loads(model_bytes)
        logs = bi.r.lrange(bi.data_key, 0, -1)

        for entry in logs:
            entry = pickle.loads(entry)
            features = [hash(entry['error_type']) % 100, hash(entry['doc_type']) % 100,
                        hash(entry['missing_field']) % 100]
            x = np.array(features).reshape(1, -1)
            pred = model.predict(x)[0]
            resolution = {"fix_field": entry['missing_field'], "value": f"predicted_{pred}"}
            payload = {"doc_id": entry['doc_id'], "resolution": resolution}

            # --- Agent 1 Call ---
            try:
                res = requests.post(bi.AGENT1_URL, json=payload)
                if res.status_code == 200:
                    bi.logger.info(f"Resolution sent to Agent1 for doc_id={entry['doc_id']}")
                else:
                    bi.logger.warning(f"Agent1 error for doc_id={entry['doc_id']}: {res.text}")
            except Exception as e:
                bi.logger.error(f"Agent1 request failed: {str(e)}")

        return {"status": "resolutions attempted"}
    except Exception as e:
        bi.logger.error(f"Prediction/Resolve Error: {str(e)}")
        return {"error": str(e)}


# Optional health check
@router.get("/health")
def health():
    return {"status": "ok"}
