# Automation Services - AI Document Processing Platform

A comprehensive AI-powered document processing platform with automated extraction, prediction services, and intelligent feedback analysis.

## 🚀 Features

- **Document Processing**: Upload and extract text from various document formats (PDF, DOC, images)
- **AI Prediction**: Machine learning models for document classification and data extraction
- **Sentiment Analysis**: Automated feedback review with sentiment detection
- **Model Management**: Continuous learning with model retraining capabilities
- **Modern UI**: React-based frontend with responsive design
- **RESTful APIs**: FastAPI-powered backend services

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 3000)
└────────┬────────┘
         │
    ┌────┴────┐
    │  Nginx  │
    └────┬────┘
         │
    ┌────┴─────────────────────┐
    │                          │
┌───┴──────────────┐  ┌────────┴─────────┐
│ Extraction API   │  │ Prediction API   │
│ (Port 8000)      │  │ (Port 8001)      │
└───┬──────────────┘  └────────┬─────────┘
    │                          │
    └────┬─────────────────────┘
         │
    ┌────┴─────┐
    │          │
┌───┴────┐ ┌──┴───┐
│ PostgreSQL│ │ Redis │
└──────────┘ └──────┘
```

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended for easiest setup)
- **OR** for local development:
  - Python 3.13+
  - Node.js 20.19+ or 22.12+
  - PostgreSQL 15+
  - Redis 7+

## 🐍 Python Virtual Environment Setup

**Important:** Before running any Python services locally, set up a virtual environment:

```bash
# Quick setup with automated script
./setup_venv.sh

# Activate the virtual environment
source venv/bin/activate
```

For detailed venv setup instructions, see [VENV_SETUP.md](VENV_SETUP.md)

## 🚀 Quick Start

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
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

### Option 3: Manual Setup

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📁 Project Structure

```
Automation_Services/
├── backend/
│   ├── extraction_service/    # Document processing API
│   ├── prediction_service/    # ML prediction API
│   ├── dashboard/             # Analytics dashboard
│   └── CRM/                   # Customer feedback service
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API integration
│   │   └── types/            # TypeScript definitions
│   └── public/               # Static assets
├── database/                 # Database models & schemas
│   ├── models.py            # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── repository/          # Data access layer
├── docker-compose.yml       # Multi-container setup
├── setup.sh                 # Automated setup script
└── DEPLOYMENT.md           # Deployment guide
```

## 🛠️ Backend Services

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

## 💻 Frontend Application

Built with React, TypeScript, and Tailwind CSS v4.

### Pages

1. **Dashboard** - Overview and statistics
2. **Document Processor** - Upload and process documents
3. **Feedback Review** - Submit and analyze feedback
4. **Model Management** - Retrain and manage AI models

### Tech Stack

- React 18
- TypeScript
- Vite
- React Router v7
- Tailwind CSS v4
- Lucide Icons
- Axios

## 🔧 Development

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

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Start dev server
npm run dev
```

## 🐳 Docker Commands

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

## 🔒 Environment Variables

### Backend (.env)

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/automation_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (frontend/.env)

```bash
VITE_API_URL=http://localhost:8000
```

## 📊 API Documentation

Once the services are running, visit:
- Extraction Service: http://localhost:8000/docs
- Prediction Service: http://localhost:8001/docs

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:
- Production Docker setup
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes configuration
- Security best practices
- Monitoring and logging

## 🐛 Troubleshooting

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

3. **Frontend can't connect to backend**
   ```bash
   # Check VITE_API_URL in frontend/.env
   # Verify CORS settings in backend
   ```

## 📝 Fixed Backend Errors

The following errors have been fixed:

1. ✅ Prediction service import errors
2. ✅ CRM service Flask/FastAPI mixing
3. ✅ Database model missing imports
4. ✅ Repository syntax errors
5. ✅ Extraction service syntax issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📧 Support

For issues and questions:
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- Review API documentation
- Check Docker logs: `docker-compose logs -f`

## 🎯 Roadmap

- [ ] Add unit tests
- [ ] Implement authentication middleware
- [ ] Add file upload progress tracking
- [ ] Implement WebSocket for real-time updates
- [ ] Add export functionality for processed documents
- [ ] Implement batch processing
- [ ] Add model versioning
- [ ] Create admin dashboard