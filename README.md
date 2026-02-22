# Basalt

Interactive 2D floor plan tool. Draw your terrain, place rooms, validate constraints, and generate layout suggestions.

## Stack

- **Frontend**: React + TypeScript + Vite + Konva.js
- **Backend**: Python + FastAPI + Shapely

## Prerequisites

- Node.js >= 20
- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Getting started

```bash
# Install all dependencies
make install

# Start both servers
make dev
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs

## Individual commands

```bash
make dev-frontend    # Frontend only
make dev-backend     # Backend only
make lint            # Lint frontend + backend
make test            # Run backend tests
```
