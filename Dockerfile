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



FROM python:3.11-slim AS base

ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

# Installer curl pour Poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# ---------------- Builder Stage ----------------
FROM base AS builder

WORKDIR /app

# 1. Installer outils de compilation pour dépendances Python
# Ajout de dépendances courantes qui font échouer la compilation (libssl-dev, zlib1g-dev)
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        git \
        build-essential \
        libffi-dev \
        libssl-dev \
        zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement fichiers de configuration pour tirer parti du cache Docker
COPY poetry.lock pyproject.toml ./
COPY README.md /app/

# 2. Installer dépendances Python
# CORRECTION CLÉ : Retrait de --no-root et utilisation de --only main
RUN poetry config virtualenvs.in-project true \
    && poetry install --only main --no-interaction \
    && rm -rf "$POETRY_HOME/cache"

# ---------------- Runner Stage ----------------
FROM base AS runner

WORKDIR /app

# Copier le virtualenv créé par le builder
# Cette ligne devrait maintenant fonctionner si le .venv est créé correctement.
COPY --from=builder /app/.venv/ /app/.venv/

# Copier le code source
COPY src /app/src

# Exposer le port
EXPOSE 8000

# Lancer l'application avec gunicorn du virtualenv
CMD ["/app/.venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.poject.api.app:app"]
