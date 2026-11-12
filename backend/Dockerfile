# ───────────────────────────────────────────
# Base stage — shared by dev and prod
# ───────────────────────────────────────────
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# ───────────────────────────────────────────
# Development stage
# ───────────────────────────────────────────
FROM base AS dev

# Re-declare PATH so Poetry is findable in this stage
ENV PATH="/opt/poetry/bin:$PATH"

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ───────────────────────────────────────────
# Production stage
# ───────────────────────────────────────────
FROM base AS prod

# Re-declare PATH so Poetry is findable in this stage
ENV PATH="/opt/poetry/bin:$PATH"

RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]