from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.cache.redis_client import redis_client
from datetime import datetime, timezone
import json
from database import schemas
from typing import Dict, Any
import uuid
import os

os.environ.setdefault("TIKA_JAVA", "/usr/lib/jvm/java-21-openjdk-amd64/bin/java")

from tika import parser
from ..services.predictor_main import predict
from ..utils import currentuser

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(tags=["doc_processor"])


@router.post("/api/upload", response_model=Dict[str, Any])
async def process_document(
    file: UploadFile = File(...),
    current_user: schemas.client.Client = Depends(currentuser.get_current_client)
):
    
    try:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        raw = parser.from_file(temp_file_path)

        metadata = str(raw.get("metadata", ""))
        text_content = raw.get("content") or perform_ocr(temp_file_path)

        output = predict(text_content)

        document_context = {
            "ocr_text": text_content[:5000],  
            "doc_type": file.content_type,
            "metadata": metadata,
            "date": datetime.now(timezone.utc).isoformat()
        }

        redis_key = f"doc_context:{current_user.email}"

        redis_client.setex(
            redis_key,
            1800, 
            json.dumps(document_context)
        )

        os.remove(temp_file_path)

        return {
            "metadata": metadata,
            "content": output,
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def perform_ocr(file_path: str) -> str:
    import pytesseract
    from PIL import Image

    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
