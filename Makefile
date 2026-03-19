.PHONY: help setup install run test test-coverage test-watch lint format clean docker-build docker-run docs

help:
	@echo "Weather Gist API - Available Commands"
	@echo "====================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup           - Create virtual environment and install dependencies"
	@echo "  make install         - Install dependencies only"
	@echo ""
	@echo "Running the Application:"
	@echo "  make run             - Start development server (localhost:8000)"
	@echo "  make run-prod        - Start production server"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test            - Run all tests"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo "  make test-watch      - Run tests in watch mode"
	@echo "  make lint            - Run type checking (mypy)"
	@echo "  make format          - Format code (black)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean           - Remove __pycache__ and .pytest_cache"
	@echo "  make docs            - Open Swagger documentation"
	@echo ""

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Environment setup complete"
	@echo "Activate with: source .venv/bin/activate"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

run-prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=app --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated in htmlcov/index.html"

test-watch:
	python -m pytest tests/ -v --tb=short -x

lint:
	mypy app/

format:
	black app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true

docker-build:
	docker build -t weather-gist-api .

docker-run:
	docker run -p 8000:8000 \
		-e OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY} \
		-e GITHUB_TOKEN=${GITHUB_TOKEN} \
		weather-gist-api

docs:
	@python -m webbrowser "http://localhost:8000/docs" 2>/dev/null || echo "Open http://localhost:8000/docs in your browser"
