# FROM python:3.11-buster
# # ⚡ Variables d'environnement
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV POETRY_HOME="/opt/poetry"
# ENV PATH="$POETRY_HOME/bin:$PATH"

# # 🛠 Installer les dépendances système nécessaires
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     git \
#     build-essential \
#     libffi-dev \
#     wget \
#     && rm -rf /var/lib/apt/lists/*
# # cmake removed here ⬆️

# # 📦 Installer Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -

# WORKDIR /app

# # 🔗 Copier seulement les fichiers de configuration d'abord pour tirer parti du cache Docker
# COPY pyproject.toml poetry.lock* /app/

# # 💡 Installer les dépendances Python
# RUN poetry install --no-root --no-interaction

# # 🧹 Supprimer le cache Poetry pour réduire la taille de l'image
# RUN rm -rf "$POETRY_HOME/cache"

# # 📂 Copier le code source et les tests
# COPY src /app/src
# COPY tests /app/tests

# # 🔌 Exposer le port
# EXPOSE 8080

# # 🚀 Lancer l'application avec gunicorn
# CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8080", "src.poject.api.app:app"]




# Base Stage (Minimal)
# Utilisé pour installer Poetry. Devient la base du Runner final.
FROM python:3.11-slim AS base

ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

# Installer les outils APTS nécessaires pour installer Poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# -----------------------------------------------------------
# Builder Stage (Heavy Lifting)
# Cette étape installe les dépendances Python et crée le Virtual Environment (.venv).
FROM base AS builder

WORKDIR /app

# 1. INSTALLER LES OUTILS DE COMPILATION CRITIQUES ICI
# Ces outils ne sont pas nécessaires au runtime et seront jetés après cette étape.
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        git \
        build-essential \
        libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./

# 2. Installer les dépendances Python dans un .venv dans le projet
RUN poetry config virtualenvs.in-project true \
    && poetry install --only main --no-interaction
RUN rm -rf "$POETRY_HOME/cache"

# -----------------------------------------------------------
# Runner Stage (Final / Production)
# Copie uniquement le code et l'environnement virtuel (.venv)
FROM base AS runner

WORKDIR /app

# Copie le .venv de l'étape 'builder' vers l'étape 'runner'
COPY --from=builder /app/.venv/ /app/.venv/

# Copie le code source
COPY src /app/src 
# Retiré 'COPY . /app/' car il inclut potentiellement des fichiers inutiles
# et utilise 'COPY src /app/src' qui est plus précis.

# 💡 Assurez-vous d'utiliser le binaire gunicorn du .venv copié
# La syntaxe est cruciale pour pointer vers le chemin exact.
CMD ["/app/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.poject.api.app:app"]
