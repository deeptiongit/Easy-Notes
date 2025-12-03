import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Config
AGENT1_URL = "http://localhost:8001"
AGENT2_URL = "http://localhost:8002"

class IncomingDoc(BaseModel):
    doc_id: str
    doc_type: str
    payload: dict

@app.post("/process_document")
def process_document(doc: IncomingDoc):

    response = requests.post(f"{AGENT1_URL}/agent1/process", json=doc.model_dump())
    if response.status_code != 200:
        return {"error": "Agent 1 failed to process"}

    agent1_result = response.json()
    if not agent1_result.get("status") == "failure":
        return {"status": "processed", "message": "No failure reported"}

    failure_payload = {
        "doc_id": doc.doc_id,
        "error_type": agent1_result["error_type"],
        "doc_type": doc.doc_type,
        "missing_field": agent1_result["missing_field"],
        "context": agent1_result.get("context", ""),
        "payload": doc.payload,
    }

    #  Step 2: Log failure to Agent 2
    requests.post(f"{AGENT2_URL}/agent2/log_failure", json=failure_payload)

    #  Step 3: Let Agent 2 try resolution
    resolution = requests.post(f"{AGENT2_URL}/agent2/predict_and_resolve").json()

    return {
        "status": "failure routed",
        "agent1_response": agent1_result,
        "agent2_resolution_status": resolution,
    }

@app.post("/feedback")
def feedback_to_agent2(feedback: dict):
    resp = requests.post(f"{AGENT2_URL}/agent2/feedback", json=feedback)
    return resp.json()
