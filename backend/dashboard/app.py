from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Dashboard Service",
    description="Analytics and monitoring dashboard",
    version="1.0.0"
)

git status
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Dashboard Service API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "dashboard-service"}

@app.get("/api/stats")
def get_stats():
    """Get system statistics"""
    return {
        "documents_processed": 1234,
        "success_rate": 94.5,
        "pending_reviews": 23,
        "model_accuracy": 96.8
    }