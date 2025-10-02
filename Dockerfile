FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
COPY src /app/src
COPY tests /app/tests

RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8080

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8080", "src.projet.api.app:app"]
