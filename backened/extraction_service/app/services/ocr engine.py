from typing import Dict, Any
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import hashlib
import redis
import traceback  
from fastapi.concurrency import run_in_threadpool
from ..services.extractor_llm import extract_fields
from ..utils import oauth2
from ..utils.Redis import r 



UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
CHUNK_SIZE = 1024 * 1024  


def preprocess_image(image: Image.Image) -> Image.Image:
    """Preprocess image for better OCR"""
    img_cv = np.array(image)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    _, binary_img = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return Image.fromarray(binary_img)

def perform_ocr( file_path):
    try:
        hasher = hashlib.md5()
        with open(temp_file_path, "wb") as buffer:
            while content := await file.read(CHUNK_SIZE):
                hasher.update(content)
                buffer.write(content)
        file_hash = hasher.hexdigest()

        cached_result = r.get(file_hash)
        if cached_result:
            return json.loads(cached_result)

        def ocr_processing_task():
            if file.content_type == "application/pdf":
                images = convert_from_path(temp_file_path)
                processed_text = []
                for image in images:
                    preprocessed_img = preprocess_image(image)
                    processed_text.append(pytesseract.image_to_string(preprocessed_img))
                return "\n".join(processed_text)
            else:
                image = Image.open(temp_file_path)
                preprocessed_img = preprocess_image(image)
                return pytesseract.image_to_string(preprocessed_img)

        ocr_text = await run_in_threadpool(ocr_processing_task)

        if not ocr_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract any text. Document may be empty or low quality."
            )

        extracted_fields = extract_fields(ocr_text)

        response_data = {"filename": file.filename, "extracted_data": extracted_fields}

        r.set(file_hash, json.dumps(response_data), ex=3600)
        return response_data
    
    except Exception as e:
        tb_str = traceback.format_exc() 
        print(f" Unexpected error in OCR:\n{tb_str}")  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: The error is heerr{str(e) }"
        )
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
