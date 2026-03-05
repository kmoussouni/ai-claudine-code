#!/bin/bash
# Télécharge des modèles Stable Diffusion populaires

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Téléchargement Modèles Stable Diffusion            ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════════╝${NC}"
echo ""

# Modèles disponibles
echo "Modèles disponibles :"
echo "  1. SD 1.5 (4 GB) - Rapide, bon pour tests"
echo "  2. SDXL 1.0 (6.5 GB) - Meilleure qualité"
echo "  3. Pixel Art LoRA (100 MB) - Style pixel art pour jeux"
echo ""

read -p "Quel modèle voulez-vous télécharger? [1-3]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}📥 Téléchargement SD 1.5...${NC}"
        echo ""
        echo "Commande à exécuter dans le conteneur:"
        echo ""
        echo "docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors \\"
        echo "  https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors"
        echo ""
        read -p "Exécuter maintenant? [o/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[OoYy]$ ]]; then
            docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors \
              https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
            echo -e "${GREEN}✅ Modèle SD 1.5 téléchargé${NC}"
        fi
        ;;
    2)
        echo ""
        echo -e "${YELLOW}📦 SDXL est très volumineux (6.5 GB)${NC}"
        echo ""
        echo "Commande à exécuter:"
        echo ""
        echo "docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/sd_xl_base_1.0.safetensors \\"
        echo "  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
        ;;
    3)
        echo ""
        echo -e "${BLUE}🎮 LoRA Pixel Art${NC}"
        echo ""
        echo "Pour installer des LoRAs :"
        echo "1. Téléchargez depuis https://civitai.com (cherchez 'pixel art lora')"
        echo "2. Placez le fichier .safetensors dans le volume sd_models/Lora/"
        echo ""
        echo "Commande exemple:"
        echo "docker-compose cp pixel-art-lora.safetensors stable-diffusion:/data/models/Lora/"
        ;;
    *)
        echo -e "${YELLOW}❌ Choix invalide${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Note :${NC} Après téléchargement, redémarrez le service:"
echo "  docker-compose restart stable-diffusion"
echo ""
