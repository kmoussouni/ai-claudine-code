#!/bin/bash
# Téléchargement des modèles FLUX

MODELS_DIR="/app/models"

echo "=== Téléchargement des modèles FLUX ==="

# Fonction pour vérifier la taille d'un fichier
check_file_size() {
    local file=$1
    local min_size=$2

    if [ ! -f "$file" ]; then
        return 1
    fi

    local size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo 0)
    if [ "$size" -lt "$min_size" ]; then
        echo "⚠️  Fichier incomplet ($size bytes < $min_size bytes), suppression..."
        rm -f "$file"
        return 1
    fi
    return 0
}

# FLUX.1-schnell (rapide, 4 steps, ~12GB = 12000000000 bytes)
MIN_SIZE_SCHNELL=11000000000  # 11GB minimum
if ! check_file_size "$MODELS_DIR/checkpoints/flux1-schnell.safetensors" $MIN_SIZE_SCHNELL; then
    echo "📥 Téléchargement FLUX.1-schnell (12GB, rapide)..."
    wget --continue --show-progress \
        "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors" \
        -O "$MODELS_DIR/checkpoints/flux1-schnell.safetensors"

    if check_file_size "$MODELS_DIR/checkpoints/flux1-schnell.safetensors" $MIN_SIZE_SCHNELL; then
        echo "✅ FLUX.1-schnell téléchargé"
    else
        echo "❌ Échec téléchargement FLUX.1-schnell"
        exit 1
    fi
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

# VAE (nécessaire pour FLUX, ~335MB)
MIN_SIZE_VAE=300000000  # 300MB minimum
if ! check_file_size "$MODELS_DIR/vae/ae.safetensors" $MIN_SIZE_VAE; then
    echo "📥 Téléchargement VAE FLUX..."
    wget --continue --show-progress \
        "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors" \
        -O "$MODELS_DIR/vae/ae.safetensors"

    if check_file_size "$MODELS_DIR/vae/ae.safetensors" $MIN_SIZE_VAE; then
        echo "✅ VAE téléchargé"
    else
        echo "❌ Échec téléchargement VAE"
        exit 1
    fi
else
    echo "✅ VAE déjà présent"
fi

# CLIP L (~1GB)
MIN_SIZE_CLIP=900000000  # 900MB minimum
if ! check_file_size "$MODELS_DIR/clip/clip_l.safetensors" $MIN_SIZE_CLIP; then
    echo "📥 Téléchargement CLIP L..."
    wget --continue --show-progress \
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors" \
        -O "$MODELS_DIR/clip/clip_l.safetensors"

    if check_file_size "$MODELS_DIR/clip/clip_l.safetensors" $MIN_SIZE_CLIP; then
        echo "✅ CLIP L téléchargé"
    else
        echo "❌ Échec téléchargement CLIP L"
        exit 1
    fi
else
    echo "✅ CLIP L déjà présent"
fi

# T5-XXL (~9GB)
MIN_SIZE_T5XXL=8500000000  # 8.5GB minimum
if ! check_file_size "$MODELS_DIR/clip/t5xxl_fp16.safetensors" $MIN_SIZE_T5XXL; then
    echo "📥 Téléchargement T5-XXL (large, ~9GB)..."
    wget --continue --show-progress \
        "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors" \
        -O "$MODELS_DIR/clip/t5xxl_fp16.safetensors"

    if check_file_size "$MODELS_DIR/clip/t5xxl_fp16.safetensors" $MIN_SIZE_T5XXL; then
        echo "✅ T5-XXL téléchargé"
    else
        echo "❌ Échec téléchargement T5-XXL"
        exit 1
    fi
else
    echo "✅ T5-XXL déjà présent"
fi

echo ""
echo "=== Modèles FLUX prêts ==="
ls -lh "$MODELS_DIR/checkpoints"/*.safetensors 2>/dev/null || echo "Aucun checkpoint trouvé"
echo ""
