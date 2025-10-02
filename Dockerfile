FROM python:3.11-slim

# ⚡ Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# 🛠 Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    cmake \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 📦 Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# 🔗 Copier seulement les fichiers de configuration d'abord pour tirer parti du cache Docker
COPY pyproject.toml poetry.lock* /app/

# 💡 Installer les dépendances Python
RUN poetry install --no-root --without dev --no-interaction

# 🧹 Supprimer le cache Poetry pour réduire la taille de l'image
RUN rm -rf "$POETRY_HOME/cache"

# 📂 Copier le code source et les tests
COPY src /app/src
COPY tests /app/tests

# 🔌 Exposer le port
EXPOSE 8080

# 🚀 Lancer l'application avec gunicorn
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8080", "poject.api.app:app"]
