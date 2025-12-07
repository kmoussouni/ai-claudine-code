#!/bin/bash
# Téléchargement des modèles FLUX

MODELS_DIR="/app/models"

echo "=== Téléchargement des modèles FLUX ==="

# FLUX.1-schnell (rapide, 4 steps, ~12GB)
if [ ! -f "$MODELS_DIR/checkpoints/flux1-schnell.safetensors" ]; then
    echo "📥 Téléchargement FLUX.1-schnell (12GB, rapide)..."
    wget -q --show-progress \
        "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors" \
        -O "$MODELS_DIR/checkpoints/flux1-schnell.safetensors"
    echo "✅ FLUX.1-schnell téléchargé"
else
    echo "✅ FLUX.1-schnell déjà présent"
fi

# FLUX.1-dev (qualité maximale, ~12GB)
# Décommenter si vous voulez la meilleure qualité (nécessite licence)
# if [ ! -f "$MODELS_DIR/checkpoints/flux1-dev.safetensors" ]; then
#     echo "📥 Téléchargement FLUX.1-dev (12GB, haute qualité)..."
#     wget -q --show-progress \
#         "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors" \
#         -O "$MODELS_DIR/checkpoints/flux1-dev.safetensors"
#     echo "✅ FLUX.1-dev téléchargé"
# fi

# VAE (nécessaire pour FLUX)
if [ ! -f "$MODELS_DIR/vae/ae.safetensors" ]; then
    echo "📥 Téléchargement VAE FLUX..."
    wget -q --show-progress \
        "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors" \
        -O "$MODELS_DIR/vae/ae.safetensors"
    echo "✅ VAE téléchargé"
else
    echo "✅ VAE déjà présent"
fi

# CLIP models
if [ ! -f "$MODELS_DIR/clip/clip_l.safetensors" ]; then
    echo "📥 Téléchargement CLIP L..."
    wget -q --show-progress \
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors" \
        -O "$MODELS_DIR/clip/clip_l.safetensors"
    echo "✅ CLIP L téléchargé"
else
    echo "✅ CLIP L déjà présent"
fi

if [ ! -f "$MODELS_DIR/clip/t5xxl_fp16.safetensors" ]; then
    echo "📥 Téléchargement T5-XXL (large, ~9GB)..."
    wget -q --show-progress \
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors" \
        -O "$MODELS_DIR/clip/t5xxl_fp16.safetensors"
    echo "✅ T5-XXL téléchargé"
else
    echo "✅ T5-XXL déjà présent"
fi

echo ""
echo "=== Modèles FLUX prêts ==="
ls -lh "$MODELS_DIR/checkpoints"/*.safetensors 2>/dev/null || echo "Aucun checkpoint trouvé"
echo ""
