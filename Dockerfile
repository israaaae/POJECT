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



# FROM python:3.11-slim

# ENV POETRY_HOME=/opt/poetry
# ENV PATH=${POETRY_HOME}/bin:${PATH}
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # Installer les dépendances système
# RUN apt-get update \
#     && apt-get install --no-install-recommends -y \
#         curl \
#         git \
#         build-essential \
#         libffi-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Installer Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -

# # Copier les fichiers de configuration
# COPY pyproject.toml poetry.lock* README.md ./

# # Copier le code source AVANT l'installation
# COPY src ./src

# # Installer les dépendances
# RUN poetry config virtualenvs.in-project true \
#     && poetry install --only main --no-interaction \
#     && rm -rf "$POETRY_HOME/cache"

# # Exposer le port
# EXPOSE 8000

# # Lancer l'application
# CMD [".venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.poject.api.app:app"]


FROM python:3.11-slim
ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer les dépendances système
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        git \
        build-essential \
        libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copier les fichiers de configuration
COPY pyproject.toml poetry.lock* README.md ./

# Copier le code source AVANT l'installation
COPY src ./src

# Installer les dépendances
RUN poetry config virtualenvs.in-project true \
    && poetry install --only main --no-interaction \
    && rm -rf "$POETRY_HOME/cache"

# Exposer le port
EXPOSE 80

# Lancer l'application
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:80", "src.poject.api.app:app"]


