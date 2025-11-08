###
# Production Dockerfile for contoso-backend
# Uses Python 3.12 slim image, installs build/runtime deps, installs package from pyproject.toml,
# copies sources, creates a non-root user and runs uvicorn.
###

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS-level build deps required for some Python packages (e.g. asyncpg, passlib backends)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libpq-dev \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project files first (pyproject) and sources so pip can build/install
COPY pyproject.toml /app/
COPY src/ /app/src/

# Upgrade pip and install the package declared in pyproject (project.dependencies)
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .

# Create a non-root user and make sure /app is owned
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Recommended environment variable: the app reads settings from envs (e.g. database URL)
ENV MODERN_API_BASE_URL=http://0.0.0.0:8000

# Production command - expose proxy headers and bind to 0.0.0.0
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
