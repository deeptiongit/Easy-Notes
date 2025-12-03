from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.extraction_service.app.routers import extract, erp, client, auth
from backend.CRM import crm
from database import models, database
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Document Processing Agent",
    description="Extraction service for document processing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(extract.router)
app.include_router(erp.router)
app.include_router(client.router)
app.include_router(crm.router)

@app.get("/")
def root():
    return {"message": "AI Document Processing API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "extraction-service"}