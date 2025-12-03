import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def predict(text: str) -> Dict[str, Any]:
    from backend.prediction_service.phi3.src.Companydoc_csvdata.preprocess import preprocess_report

    try:
        logger.info("Processing text with predictor")
        result = preprocess_report(text)
        return result
    except Exception as exc:
        logger.error("Prediction failed: %s", exc)
        return {
            "error": str(exc),
            "Value": "NULL",
        }