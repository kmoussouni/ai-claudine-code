# Dockerfile pour Stable Diffusion WebUI (AUTOMATIC1111)
FROM python:3.10-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Cloner AUTOMATIC1111 Stable Diffusion WebUI
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git .

# Installer PyTorch CPU d'abord
RUN pip install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Puis installer les autres dépendances depuis PyPI
RUN pip install --no-cache-dir \
    transformers \
    diffusers \
    accelerate \
    safetensors \
    omegaconf \
    pytorch-lightning \
    scikit-image \
    timm \
    piexif \
    einops \
    jsonmerge \
    clean-fid \
    resize-right \
    tomesd \
    kornia \
    lark \
    inflection \
    GitPython \
    torchsde \
    psutil \
    httpx \
    fastapi \
    uvicorn

# Créer les répertoires nécessaires
RUN mkdir -p /data/models /outputs /workspace/generated-images

# Exposer le port
EXPOSE 7860

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1

# Lancer le serveur
CMD ["python", "launch.py", "--listen", "--port", "7860", "--api", "--no-half", "--skip-torch-cuda-test", "--skip-version-check"]
