FROM python:3.14-slim

WORKDIR /app

# Install system tools + Node.js LTS
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONPATH=/app/backend/src

# Copy only dependency files first (for caching)
# Copy entire application (backend + frontend)
COPY . .
# Install backend dependencies
RUN uv pip install --system --requirements backend/pyproject.toml



# Expose backend + frontend ports
EXPOSE 8000 5173

# Default command for development mode
# Runs both backend (Uvicorn reload) & frontend (npm run dev)
CMD ["bash", "-c", "\
    cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload & \
    cd webapp && npm install && npm run dev -- --host 0.0.0.0 \
"]
