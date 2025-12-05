#!/bin/bash
# Claudine Agent - Mode Aider Direct
# Wrapper pour utiliser Aider directement avec Ollama

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_MODEL=${DEFAULT_MODEL:-"qwen2.5-coder:7b"}
OLLAMA_URL=${OLLAMA_BASE_URL:-"http://localhost:11434"}
WORKSPACE_DIR="workspace"

# Banner
echo -e "${BLUE}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║           Claudine - Agent Aider Direct                  ║
║              Mode CLI Natif avec Aider                   ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Vérifier qu'Aider est installé dans le container
echo -e "${CYAN}🔍 Vérification des services...${NC}"

# Vérifier que les services Docker tournent
if ! docker-compose ps | grep -q "claudine-ollama.*Up"; then
    echo -e "${RED}❌ Le service Ollama n'est pas démarré${NC}"
    echo -e "${YELLOW}   Lancez: make start${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Services en ligne${NC}"

# Afficher les modèles disponibles
echo -e "${CYAN}📦 Modèles disponibles:${NC}"
docker-compose exec -T ollama ollama list 2>/dev/null | tail -n +2 | awk '{print "   - " $1}'

echo ""
echo -e "${YELLOW}Modèle actuel: ${BOLD}${DEFAULT_MODEL}${NC}"
echo -e "${YELLOW}Workspace: ${BOLD}${WORKSPACE_DIR}${NC}"
echo ""
echo -e "${CYAN}💡 Commandes Aider utiles:${NC}"
echo "   /help         - Aide complète"
echo "   /add <file>   - Ajouter un fichier au contexte"
echo "   /drop <file>  - Retirer un fichier"
echo "   /ls           - Lister les fichiers en contexte"
echo "   /clear        - Effacer l'historique"
echo "   /exit         - Quitter"
echo ""
echo -e "${GREEN}🚀 Démarrage d'Aider...${NC}"
echo ""

# Lancer Aider dans le container avec terminal interactif
docker-compose exec code-agent bash -c "cd /workspace && aider \
    --model ollama/${DEFAULT_MODEL} \
    --no-auto-commits \
    --dark-mode \
    $@"

echo ""
echo -e "${GREEN}👋 Session Aider terminée${NC}"
