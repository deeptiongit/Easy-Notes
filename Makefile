.PHONY: help docker-up docker-down docker-build docker-logs clean test

help:
	@echo "Available commands:"
	@echo "  make docker-build   - Build all Docker images"
	@echo "  make docker-up      - Start all services"
	@echo "  make docker-down    - Stop all services"
	@echo "  make docker-logs    - Show logs for all services"
	@echo "  make clean          - Clean Docker and cache"
	@echo "  make test           - Run tests inside backend containers"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	docker-compose run --rm crm pytest

OUTDIR ?= ./tmp_retrain_model
DATAFILE ?= ./test_sample.csv



