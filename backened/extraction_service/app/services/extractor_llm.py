from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from transformers import pipeline
from ..utils.Redis import r 
import os
import hashlib
import redis
import json


pipe = pipeline("text-generation", model="google/gemma-3-270m")


prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a strict JSON generator. Always return ONLY a valid JSON object, "
     "with no text outside JSON. If a field cannot be found, set it to null."),
    ("user", 
     """Extract the following fields from the OCR text:

Required Fields:
- invoice_number (string)
- invoice_date (YYYY-MM-DD)
- vendor_name (string)
- total_amount (float)
- line_items (array of {{"description": string, "amount": float}})

OCR TEXT:
{ocr_text}
""")
])

hf_pipe = HuggingFacePipeline(pipeline=pipe)

def safe_json_parser(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            cleaned = text[text.find("{"): text.rfind("}") + 1]
            return json.loads(cleaned)
        except Exception:
            return {"error": "Invalid JSON", "raw_output": text}

chain = (
    {"ocr_text": RunnablePassthrough()}
    | prompt
    | hf_pipe
    | RunnableLambda(safe_json_parser)
)


def extract_fields(ocr_text: str):
    key = hashlib.md5(ocr_text.encode()).hexdigest()
    
    cached = r.get(key)
    if cached:
        return json.loads(cached)  

    result = chain.invoke( ocr_text)
    
    if "error" not in result:
        r.set(key, json.dumps(result), ex=3600)
    
    return result