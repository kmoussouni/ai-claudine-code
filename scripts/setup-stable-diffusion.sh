#!/bin/bash
# Setup Stable Diffusion pour Claudine
# Télécharge les modèles de base et configure le service

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Setup Stable Diffusion pour Claudine               ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérifier que docker-compose tourne
if ! docker-compose ps | grep -q "claudine-sd"; then
    echo -e "${YELLOW}⚠️  Le service Stable Diffusion n'est pas démarré${NC}"
    echo "Démarrage du service..."
    docker-compose up -d stable-diffusion
    echo ""
    echo -e "${GREEN}✅ Service démarré${NC}"
    echo -e "${YELLOW}⏳ Attendez 30-60 secondes que le service soit prêt...${NC}"
    sleep 30
fi

# Attendre que l'API soit disponible
echo ""
echo -e "${BLUE}🔍 Vérification de l'API Stable Diffusion...${NC}"

MAX_RETRIES=10
RETRY=0

while [ $RETRY -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:7860/sdapi/v1/sd-models >/dev/null 2>&1; then
        echo -e "${GREEN}✅ API Stable Diffusion disponible !${NC}"
        break
    fi

    RETRY=$((RETRY + 1))
    echo -e "${YELLOW}⏳ Tentative $RETRY/$MAX_RETRIES...${NC}"
    sleep 5
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    echo -e "${YELLOW}❌ L'API n'est pas encore disponible${NC}"
    echo "Le service est en train de démarrer, cela peut prendre quelques minutes."
    echo "Vérifiez les logs avec: docker-compose logs stable-diffusion"
    exit 1
fi

# Lister les modèles disponibles
echo ""
echo -e "${BLUE}📦 Modèles Stable Diffusion installés :${NC}"
curl -s http://localhost:7860/sdapi/v1/sd-models | python3 -c "
import sys, json
models = json.load(sys.stdin)
if not models:
    print('   ⚠️  Aucun modèle installé')
    print('')
    print('   Pour installer des modèles :')
    print('   1. Téléchargez un modèle depuis https://civitai.com')
    print('   2. Placez le fichier .safetensors dans le volume sd_models')
    print('   3. Redémarrez le service: docker-compose restart stable-diffusion')
else:
    for model in models:
        print(f\"   - {model['model_name']}\")
"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        Stable Diffusion Setup Terminé !                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Interface Web: http://localhost:7860"
echo "API Docs: http://localhost:7860/docs"
echo ""
echo "Prochaines étapes:"
echo "  1. Télécharger un modèle (voir scripts/download-sd-models.sh)"
echo "  2. Tester la génération d'images depuis l'interface web"
echo "  3. Intégrer avec l'agent API"
echo ""
