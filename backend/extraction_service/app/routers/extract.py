from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from database import schemas
from typing import Dict, Any
import uuid
import os

# Ensure tika-python knows exactly which Java binary to use to avoid PATH issues.
os.environ.setdefault("TIKA_JAVA", "/usr/lib/jvm/java-21-openjdk-amd64/bin/java")

from tika import parser
from ..services.predictor_main import predict
from ..utils import oauth2

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/proc", tags=["doc_processor"])

@router.post("/doc_processing/", response_model=Dict[str, Any])
async def process_document(
    file: UploadFile = File(...),
    current_user: schemas.Client = Depends(oauth2.get_current_user)
):
    try:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        raw = parser.from_file(temp_file_path)
        metadata = ""
        text_content = ""
        
        if raw.get('content'):
            metadata = str(raw.get('metadata', ''))
            text_content = raw['content']
        else:
            text_content = perform_ocr(temp_file_path)
        
        output = predict(text_content)
        
        os.remove(temp_file_path)
        
        return {
            'metadata': metadata,
            'content': output,
            'filename': file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def perform_ocr(file_path: str) -> str:
    import pytesseract
    from PIL import Image
    
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")