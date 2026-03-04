#!/bin/bash
# Téléchargement des modèles FLUX
# Nécessite un token HuggingFace (gratuit) :
#   1. Créer un compte sur https://huggingface.co
#   2. Accepter la licence FLUX : https://huggingface.co/black-forest-labs/FLUX.1-schnell
#   3. Générer un token : https://huggingface.co/settings/tokens
#   4. Passer HF_TOKEN en variable d'environnement

set -euo pipefail

MODELS_DIR="/app/models"

echo "=== Téléchargement des modèles FLUX ==="

if [ -z "${HF_TOKEN:-}" ]; then
    echo "⚠️  HF_TOKEN non défini."
    echo "   Obtenez un token sur https://huggingface.co/settings/tokens"
    echo "   et définissez HF_TOKEN dans votre .env"
    echo "   Tentative sans token (peut échouer pour les modèles avec licence)..."
    AUTH_HEADER=""
else
    echo "✅ HF_TOKEN détecté"
    AUTH_HEADER="Authorization: Bearer ${HF_TOKEN}"
fi

# Wrapper de téléchargement avec curl
hf_download() {
    local url="$1"
    local output="$2"
    local min_size="${3:-0}"

    # Vérifier si le fichier existe déjà et est valide
    if [ -f "$output" ]; then
        local size
        size=$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output" 2>/dev/null || echo 0)
        if [ "$size" -ge "$min_size" ]; then
            echo "✅ $(basename "$output") déjà présent ($(numfmt --to=iec-i --suffix=B "$size"))"
            return 0
        else
            echo "⚠️  $(basename "$output") incomplet ($size bytes), re-téléchargement..."
            rm -f "$output"
        fi
    fi

    echo "📥 Téléchargement $(basename "$output")..."
    if [ -n "${AUTH_HEADER:-}" ]; then
        curl -L --progress-bar \
            --header "$AUTH_HEADER" \
            --retry 3 --retry-delay 5 \
            -o "$output" "$url"
    else
        curl -L --progress-bar \
            --retry 3 --retry-delay 5 \
            -o "$output" "$url"
    fi

    # Vérifier après téléchargement
    local final_size
    final_size=$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output" 2>/dev/null || echo 0)
    if [ "$final_size" -ge "$min_size" ]; then
        echo "✅ $(basename "$output") téléchargé ($(numfmt --to=iec-i --suffix=B "$final_size"))"
    else
        echo "❌ Échec : $(basename "$output") trop petit ($final_size bytes < $min_size)"
        rm -f "$output"
        exit 1
    fi
}

# FLUX.1-schnell — unet uniquement (~12GB)
hf_download \
    "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors" \
    "$MODELS_DIR/unet/flux1-schnell.safetensors" \
    11000000000

# VAE (~335MB)
hf_download \
    "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors" \
    "$MODELS_DIR/vae/ae.safetensors" \
    300000000

# CLIP-L (~235MB)
hf_download \
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors" \
    "$MODELS_DIR/clip/clip_l.safetensors" \
    200000000

# T5-XXL fp16 (~9GB) — encodeur texte principal de FLUX
hf_download \
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors" \
    "$MODELS_DIR/clip/t5xxl_fp16.safetensors" \
    8500000000

echo ""
echo "=== Modèles FLUX prêts ==="
echo "Unet:"
ls -lh "$MODELS_DIR/unet/"*.safetensors 2>/dev/null || echo "  (aucun)"
echo "VAE:"
ls -lh "$MODELS_DIR/vae/"*.safetensors 2>/dev/null || echo "  (aucun)"
echo "CLIP:"
ls -lh "$MODELS_DIR/clip/"*.safetensors 2>/dev/null || echo "  (aucun)"
echo ""
