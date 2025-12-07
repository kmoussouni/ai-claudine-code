# Dockerfile pour ComfyUI avec FLUX
FROM python:3.11-slim

# Dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cloner ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git . && \
    pip install --no-cache-dir -r requirements.txt

# Installer les dépendances supplémentaires
RUN pip install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    aiohttp \
    einops \
    transformers \
    safetensors \
    accelerate

# Script de téléchargement des modèles FLUX
COPY download-flux-models.sh /app/download-flux-models.sh
RUN chmod +x /app/download-flux-models.sh

# Créer les dossiers nécessaires
RUN mkdir -p /app/models/checkpoints \
             /app/models/vae \
             /app/models/clip \
             /app/output \
             /workspace/generated-images

EXPOSE 8188

# Démarrage : télécharger les modèles puis lancer ComfyUI
CMD ["/bin/bash", "-c", "/app/download-flux-models.sh && python main.py --listen 0.0.0.0 --port 8188"]
