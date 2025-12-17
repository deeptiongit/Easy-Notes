FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/prediction_service ./backend/prediction_service
COPY database ./database

RUN mkdir -p /app/models

EXPOSE 8000

CMD ["uvicorn", "backend.prediction_service.api.main:app", "--host", "0.0.0.0", "--port", "8300"]