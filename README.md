# Automation Services - AI Document Processing Platform

A comprehensive AI-powered document processing platform with automated extraction, prediction services, and intelligent feedback analysis.

##  Features

- **Document Processing**: Upload and extract text from various document formats (PDF, DOC, images)
- **AI Prediction**: Machine learning models for document classification and data extraction
- **Sentiment Analysis**: Automated feedback review with sentiment detection
- **Model Management**: Continuous learning with model retraining capabilities
- **Modern UI**: React-based frontend with responsive design
- **RESTful APIs**: FastAPI-powered backend services


```

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended for easiest setup)
- **OR** for local development:
  - Python 3.13+


##  Python Virtual Environment Setup

**Important:** Before running any Python services locally, set up a virtual environment:



# Activate the virtual environment
source venv/bin/activate
```


##  Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh
```

Follow the interactive prompts to choose your deployment option.

### Option 2: Docker Compose

```bash
# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

Access the application:
- **API Documentation**: http://localhost:8000/docs


##  Project Structure

```
Automation_Services/
├── backend/
│   ├── extraction_service/    # Document processing API
│   ├── prediction_service/    # ML prediction API
│   ├── dashboard/             # Analytics dashboard
│   └── CRM/                   # Customer feedback service
├── database/                 # Database models & schemas
│   ├── models.py            # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── repository/          # Data access layer
├── docker-compose.yml       # Multi-container setup
├── setup.sh                 # Automated setup script
└── DEPLOYMENT.md           # Deployment guide
```

##  Backend Services

### Extraction Service (Port 8000)

- Document upload and processing
- OCR text extraction
- Metadata extraction
- Tika integration for multiple formats

**Endpoints:**
- `POST /proc/doc_processing/` - Process documents
- `POST /api/login` - User authentication

### Prediction Service (Port 8001)

- Forward message processing
- Backward model updates
- Fallback LLM integration
- Continuous model training

**Endpoints:**
- `POST /api/forward` - Forward prediction
- `POST /api/backward` - Model retraining

### CRM Service

- Sentiment analysis
- Feedback collection
- Automated response generation

**Endpoints:**
- `POST /crm/api/review` - Submit feedback
- `POST /crm/api/sentiment` - Analyze sentiment


##  Development

### Backend Development

```bash
# Install dependencies
pip install uv
uv pip install -e .

# Start database services
docker-compose up -d db redis

# Run extraction service
cd backend/extraction_service
uvicorn app.main:app --reload --port 8000

# Run prediction service (new terminal)
cd backend/prediction_service
uvicorn api.main:app --reload --port 8001
```

##  Docker Commands

```bash
# Build and start
docker-compose up --build -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Restart a service
docker-compose restart [service-name]

# Scale a service
docker-compose up -d --scale extraction-service=3
```

##  Environment Variables

### Backend (.env)

```bash
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (frontend/.env)

```bash
VITE_API_URL=http://localhost:8000
```

##  API Documentation

Once the services are running, visit:
- Extraction Service: http://localhost:8000/docs
- Prediction Service: http://localhost:8001/docs

##  Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

##  Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change ports in docker-compose.yml
   ```

2. **Database connection error**
   ```bash
   # Verify DATABASE_URL in .env
   docker-compose logs db
   ```

##  Fixed Backend Errors

The following errors have been fixed:

1.  Prediction service import errors
2.  CRM service Flask/FastAPI mixing
3.  Database model missing imports
4.  Repository syntax errors
5.  Extraction service syntax issues

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



