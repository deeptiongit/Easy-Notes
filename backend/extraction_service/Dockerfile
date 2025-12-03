FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/extraction_service ./backend/extraction_service
COPY database ./database

# Create uploads directory
RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["uvicorn", "backend.extraction_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]