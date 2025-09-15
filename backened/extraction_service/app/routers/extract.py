from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from database import schemas
import uuid
import os
from tika import parser
import json

router = APIRouter(prefix="/proc", tags=["doc_processor"])

@router.post("/doc processing/", response_model=Dict[str, Any])
async def extract_text( file: UploadFile = File(...), 
    current_user: schemas.Client = Depends(oauth2.get_current_user)):

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_file_path = os.path.join(UPLOAD_DIR, unique_filename)

    raw = parser.from_file(temp_file_path)
    
    if raw["content"]:
        text = raw.get("content", "")
        return nlp_func(text)

    else:
        return perform_ocr(temp_file_path)




