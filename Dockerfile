FROM python:3.11-slim
ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        git \
        build-essential \
        libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* README.md ./

COPY src ./src
COPY src/poject/templates ./src/poject/templates

RUN poetry config virtualenvs.in-project true \
    && poetry config cache-dir /tmp \
    && poetry install --only main --no-interaction --no-cache \
    && rm -rf "$POETRY_HOME/cache" \
    && rm -rf /tmp/pypoetry \
    && rm -rf /root/.cache/pypoetry

EXPOSE 8080
CMD ["/app/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "src.poject.api.app:app"]