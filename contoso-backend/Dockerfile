#
# Production Dockerfile for contoso-backend using uv and multi-stage builds
#
# Stage 1: builder
# - Uses the official astral/uv image to install dependencies into a virtual environment.
# - This keeps build tools and dependencies out of the final production image.
#
FROM astral/uv:0.2.19-python3.12 AS builder

WORKDIR /app

# Copy only the dependency definition file first to leverage Docker's layer caching.
COPY pyproject.toml uv.lock* ./

# Create a virtual environment and install dependencies into it.
# --system-site-packages allows the venv to access system-level packages if needed.
RUN uv venv --seed && \
    uv sync --no-cache --require-hashes -p .venv

#
# Stage 2: final
# - Uses a slim Python base image for a smaller footprint.
# - Copies the virtual environment from the builder stage.
# - Creates a non-root user for security.
# - Copies the application source code.
#
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add the virtual environment's scripts directory to the PATH.
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install runtime OS dependencies required by packages like asyncpg.
# Using --no-install-recommends keeps the image lean.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the virtual environment with all installed packages from the builder stage.
COPY --from=builder /app/.venv .venv

# Create a non-root user for running the application.
RUN useradd --create-home --shell /bin/bash appuser
COPY --chown=appuser:appuser src/ ./src/

# Switch to the non-root user.
USER appuser

EXPOSE 8000

# Production command to run the application using uvicorn.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]