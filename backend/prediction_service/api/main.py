from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .forward import endpoints as forward_endpoints
from .backward import endpoints as backward_endpoints
from database import models, database
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Prediction Service",
    description="AI model prediction and training service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(forward_endpoints.router, prefix="/api", tags=["Forward Processing"])
app.include_router(backward_endpoints.router, prefix="/api", tags=["Model Training"])

@app.get("/")
def root():
    return {"message": "Prediction Service API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "prediction-service"}