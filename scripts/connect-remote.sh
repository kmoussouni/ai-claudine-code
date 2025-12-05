#!/bin/bash
# Script de connexion au serveur Claudine distant via tunnel SSH

set -e

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration par défaut
REMOTE_HOST="${CLAUDINE_REMOTE_HOST:-}"
REMOTE_USER="${CLAUDINE_REMOTE_USER:-$USER}"
SSH_KEY="${CLAUDINE_SSH_KEY:-$HOME/.ssh/id_rsa}"

# Ports à tunneler
API_PORT=3000
OLLAMA_PORT=11434
WEBUI_PORT=8080

# Fichier PID pour le tunnel
TUNNEL_PID_FILE="/tmp/claudine-tunnel.pid"

show_usage() {
    echo "Usage: $0 [start|stop|status] [options]"
    echo ""
    echo "Options:"
    echo "  -h, --host HOST     Serveur distant (ex: monserveur.com)"
    echo "  -u, --user USER     Utilisateur SSH (défaut: $USER)"
    echo "  -k, --key PATH      Chemin vers la clé SSH"
    echo ""
    echo "Variables d'environnement:"
    echo "  CLAUDINE_REMOTE_HOST   Hôte du serveur"
    echo "  CLAUDINE_REMOTE_USER   Utilisateur SSH"
    echo "  CLAUDINE_SSH_KEY       Chemin de la clé SSH"
    echo ""
    echo "Exemples:"
    echo "  $0 start --host 192.168.1.100"
    echo "  $0 start --host monserveur.com --user karim"
    echo "  CLAUDINE_REMOTE_HOST=server.com $0 start"
}

start_tunnel() {
    if [ -z "$REMOTE_HOST" ]; then
        echo -e "${RED}❌ Erreur: HOST non spécifié${NC}"
        echo "Utilisez --host ou définissez CLAUDINE_REMOTE_HOST"
        show_usage
        exit 1
    fi

    # Vérifier si un tunnel existe déjà
    if [ -f "$TUNNEL_PID_FILE" ]; then
        PID=$(cat "$TUNNEL_PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Un tunnel est déjà actif (PID: $PID)${NC}"
            echo "Utilisez '$0 stop' pour l'arrêter d'abord"
            exit 1
        else
            rm -f "$TUNNEL_PID_FILE"
        fi
    fi

    echo -e "${BLUE}🔐 Connexion au serveur Claudine distant${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "  Serveur : $REMOTE_USER@$REMOTE_HOST"
    echo "  Clé SSH : $SSH_KEY"
    echo ""
    echo "  Tunnels créés:"
    echo "    localhost:$API_PORT      → API Claudine"
    echo "    localhost:$OLLAMA_PORT   → Ollama"
    echo "    localhost:$WEBUI_PORT    → Web UI"
    echo ""

    # Créer le tunnel SSH en arrière-plan
    ssh -f -N \
        -i "$SSH_KEY" \
        -L $API_PORT:localhost:$API_PORT \
        -L $OLLAMA_PORT:localhost:$OLLAMA_PORT \
        -L $WEBUI_PORT:localhost:$WEBUI_PORT \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        "$REMOTE_USER@$REMOTE_HOST"

    # Sauvegarder le PID
    # Trouver le PID du tunnel SSH
    sleep 1
    TUNNEL_PID=$(pgrep -f "ssh.*$REMOTE_HOST.*$API_PORT:localhost:$API_PORT" | tail -1)

    if [ -z "$TUNNEL_PID" ]; then
        echo -e "${RED}❌ Erreur: Impossible de créer le tunnel${NC}"
        exit 1
    fi

    echo "$TUNNEL_PID" > "$TUNNEL_PID_FILE"

    echo -e "${GREEN}✅ Tunnel SSH établi !${NC}"
    echo ""
    echo "Les agents CLI peuvent maintenant se connecter au serveur distant."
    echo ""
    echo "Commandes disponibles:"
    echo "  python3 scripts/claudine-smart.py     # Agent Smart"
    echo "  python3 scripts/agent-interactive.py  # Agent Interactif"
    echo "  open http://localhost:8080            # Web UI"
    echo ""
    echo "Pour arrêter le tunnel: $0 stop"
}

stop_tunnel() {
    if [ ! -f "$TUNNEL_PID_FILE" ]; then
        echo -e "${YELLOW}⚠️  Aucun tunnel actif${NC}"
        exit 0
    fi

    PID=$(cat "$TUNNEL_PID_FILE")

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${BLUE}🛑 Arrêt du tunnel SSH...${NC}"
        kill "$PID"
        rm -f "$TUNNEL_PID_FILE"
        echo -e "${GREEN}✅ Tunnel arrêté${NC}"
    else
        echo -e "${YELLOW}⚠️  Le tunnel n'est plus actif${NC}"
        rm -f "$TUNNEL_PID_FILE"
    fi
}

show_status() {
    if [ ! -f "$TUNNEL_PID_FILE" ]; then
        echo -e "${YELLOW}Status: Tunnel non actif${NC}"
        exit 0
    fi

    PID=$(cat "$TUNNEL_PID_FILE")

    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}Status: Tunnel actif (PID: $PID)${NC}"
        echo ""
        echo "Ports tunnelés:"
        lsof -i :$API_PORT -i :$OLLAMA_PORT -i :$WEBUI_PORT 2>/dev/null | grep LISTEN || echo "  (aucun port en écoute locale)"
    else
        echo -e "${RED}Status: Tunnel mort (PID invalide)${NC}"
        rm -f "$TUNNEL_PID_FILE"
    fi
}

# Parsing des arguments
COMMAND=""

while [[ $# -gt 0 ]]; do
    case $1 in
        start|stop|status)
            COMMAND=$1
            shift
            ;;
        -h|--host)
            REMOTE_HOST="$2"
            shift 2
            ;;
        -u|--user)
            REMOTE_USER="$2"
            shift 2
            ;;
        -k|--key)
            SSH_KEY="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo "Option inconnue: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Exécuter la commande
case $COMMAND in
    start)
        start_tunnel
        ;;
    stop)
        stop_tunnel
        ;;
    status)
        show_status
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
