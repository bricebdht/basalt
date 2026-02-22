.PHONY: dev dev-frontend dev-backend lint lint-frontend lint-backend test test-backend install

# Launch both servers in parallel
dev:
	@echo "Starting frontend and backend..."
	@make -j2 dev-frontend dev-backend

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uv run uvicorn basalt.main:app --reload --port 8000

# Install all dependencies
install:
	cd frontend && npm install
	cd backend && uv sync

# Lint
lint: lint-frontend lint-backend

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && uv run ruff check src/

# Tests
test: test-backend

test-backend:
	cd backend && uv run pytest
