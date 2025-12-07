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
RUN git clone https://github.com/comfyanonymous/ComfyUI.git .

# Installer PyTorch CPU (léger)
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Installer les requirements de ComfyUI
RUN pip install --no-cache-dir -r requirements.txt

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

# Variables d'environnement pour forcer CPU
ENV CUDA_VISIBLE_DEVICES=""
ENV FORCE_CPU=1

# Démarrage : télécharger les modèles puis lancer ComfyUI en mode CPU
CMD ["/bin/bash", "-c", "/app/download-flux-models.sh && python main.py --listen 0.0.0.0 --port 8188 --cpu"]
