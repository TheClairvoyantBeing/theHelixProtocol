.PHONY: install dev backend frontend test build clean help

# Default vault directory for local development
VAULT_DIR ?= ~/Documents/HelixVault

help:
	@echo "HELIX OS - Development Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install    Install all dependencies (Python + Node)"
	@echo "  make dev        Run backend and frontend concurrently"
	@echo "  make backend    Run FastAPI backend"
	@echo "  make frontend   Run Vite frontend"
	@echo "  make build      Build frontend for production"
	@echo "  make test       Run backend tests"
	@echo "  make clean      Remove caches and temp files"

install:
	poetry install
	cd frontend && npm install

backend:
	poetry run python -m helix.main

frontend:
	cd frontend && npm run dev

dev:
	@echo "Starting HELIX in dev mode..."
	@echo "Make sure you have Ollama running!"
	# Use & for background in bash, but for portability we suggest running in separate terminals
	@echo "Please run 'make backend' and 'make frontend' in separate terminals."

build:
	cd frontend && npm run build

test:
	poetry run pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf frontend/dist
	rm -rf frontend/node_modules
	rm -rf .venv
