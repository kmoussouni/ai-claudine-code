#!/bin/bash
# Script pour télécharger les modèles SD au premier démarrage

MODELS_DIR="/app/models/Stable-diffusion"
mkdir -p "$MODELS_DIR"

echo "=== Téléchargement des modèles Stable Diffusion ==="

# Modèle 1 : SD v1.5 (rapide, léger - 4GB)
if [ ! -f "$MODELS_DIR/v1-5-pruned-emaonly.safetensors" ]; then
    echo "📥 Téléchargement SD v1.5 (4GB)..."
    wget -q --show-progress \
        "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" \
        -O "$MODELS_DIR/v1-5-pruned-emaonly.safetensors"
    echo "✅ SD v1.5 téléchargé"
else
    echo "✅ SD v1.5 déjà présent"
fi

# Modèle 2 : SDXL (haute qualité - 7GB)
if [ ! -f "$MODELS_DIR/sd_xl_base_1.0.safetensors" ]; then
    echo "📥 Téléchargement SDXL Base (7GB)..."
    wget -q --show-progress \
        "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \
        -O "$MODELS_DIR/sd_xl_base_1.0.safetensors"
    echo "✅ SDXL Base téléchargé"
else
    echo "✅ SDXL Base déjà présent"
fi

echo ""
echo "=== Modèles disponibles ==="
ls -lh "$MODELS_DIR"/*.safetensors
echo ""
