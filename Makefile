.PHONY: help build up down logs test lint format clean migrate db-reset

help:
	@echo "Personal Longevity Team - Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  make up                Build and start all services"
	@echo "  make down              Stop all services"
	@echo "  make logs              View logs from all services"
	@echo "  make logs-api          View API logs only"
	@echo ""
	@echo "Database:"
	@echo "  make migrate           Run Alembic migrations"
	@echo "  make db-reset          Drop and recreate database"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test              Run pytest"
	@echo "  make test-cov          Run pytest with coverage"
	@echo "  make lint              Run black, isort, mypy checks"
	@echo "  make format            Format code with black and isort"
	@echo ""
	@echo "Production:"
	@echo "  make build-prod        Build production image"
	@echo "  make up-prod           Start production stack"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean             Remove containers and volumes"
	@echo "  make clean-all         Remove everything including images"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

test:
	docker-compose exec api pytest tests/ -v

test-cov:
	docker-compose exec api pytest tests/ -v --cov=src --cov-report=html

lint:
	docker-compose exec api bash -c "black --check src tests && isort --check-only src tests && mypy src"

format:
	docker-compose exec api bash -c "black src tests && isort src tests"

migrate:
	docker-compose exec api alembic upgrade head

db-reset:
	docker-compose exec api bash -c "alembic downgrade base && alembic upgrade head"

build-prod:
	docker build -f Dockerfile -t plt-api:prod .

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

clean:
	docker-compose down -v

clean-all:
	docker-compose down -v --rmi all
