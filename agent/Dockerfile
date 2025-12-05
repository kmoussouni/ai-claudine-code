FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installation des outils de développement Python
RUN pip install --no-cache-dir \
    aider-chat \
    litellm \
    fastapi \
    uvicorn \
    python-dotenv \
    httpx

# Copier les fichiers de configuration
COPY . /app/

# Créer les répertoires nécessaires
RUN mkdir -p /workspace /app/config

# Port pour l'API
EXPOSE 3000

# Script de démarrage
CMD ["python", "server.py"]
