#!/bin/bash
# Installation du Client Léger Claudine
# Pour utilisation distante sans Docker

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Installation Client Léger Claudine                  ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 non trouvé${NC}"
    echo "Installez Python 3 : https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 trouvé: $(python3 --version)${NC}"

# Créer un répertoire client si on n'est pas déjà dans le repo
if [ ! -f "claudine-agent" ]; then
    echo ""
    echo -e "${BLUE}📦 Mode Installation Client Léger${NC}"
    echo ""
    echo "Ce script va installer seulement les agents CLI,"
    echo "sans Docker ni services locaux."
    echo ""
    read -p "Continuer? [o/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[OoYy]$ ]]; then
        exit 1
    fi
fi

# Installer les dépendances Python
echo ""
echo -e "${BLUE}📚 Installation des dépendances Python...${NC}"

if [ -f "requirements-cli.txt" ]; then
    pip3 install --user -r requirements-cli.txt
    echo -e "${GREEN}✅ Dépendances installées depuis requirements-cli.txt${NC}"
else
    echo -e "${YELLOW}⚠️  requirements-cli.txt non trouvé, installation manuelle${NC}"
    pip3 install --user httpx textual rich pygments
    echo -e "${GREEN}✅ Dépendances installées${NC}"
fi

# Copier la configuration client
if [ -f ".env.client" ]; then
    if [ ! -f ".env" ]; then
        cp .env.client .env
        echo -e "${GREEN}✅ Configuration client créée (.env)${NC}"
        echo -e "${YELLOW}⚠️  N'oubliez pas de configurer l'URL du serveur dans .env${NC}"
    else
        echo -e "${YELLOW}⚠️  .env existe déjà, configuration conservée${NC}"
    fi
fi

# Vérifier que les scripts CLI sont présents
SCRIPTS_OK=true
for script in scripts/claudine-smart.py scripts/agent-interactive.py scripts/agent-tui.py scripts/connect-remote.sh; do
    if [ ! -f "$script" ]; then
        echo -e "${YELLOW}⚠️  $script non trouvé${NC}"
        SCRIPTS_OK=false
    fi
done

if $SCRIPTS_OK; then
    echo -e "${GREEN}✅ Tous les agents CLI sont présents${NC}"
else
    echo -e "${YELLOW}⚠️  Certains agents sont manquants${NC}"
    echo "Clonez le repo complet : git clone https://github.com/kmoussouni/ai-claudine-code.git"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            Installation Client Terminée !                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Configuration requise dans .env :"
echo "  1. CLAUDINE_API_URL=http://localhost:3000"
echo "  2. OLLAMA_API_BASE=http://localhost:11434"
echo "  3. CLAUDINE_REMOTE_HOST=votre-serveur.com"
echo ""
echo "Connexion au serveur distant :"
echo "  ./scripts/connect-remote.sh start --host votre-serveur.com"
echo ""
echo "Utilisation des agents :"
echo "  python3 scripts/claudine-smart.py     # Agent recommandé"
echo "  python3 scripts/agent-interactive.py"
echo "  python3 scripts/agent-tui.py"
echo ""
echo "Documentation complète :"
echo "  less REMOTE-SETUP.md"
