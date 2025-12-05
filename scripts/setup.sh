#!/bin/bash
# Script d'installation et de configuration initiale de Claudine

set -e

echo "🚀 Configuration de Claudine - Agent de code local"
echo "=================================================="

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    echo "   https://www.docker.com/get-started"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

echo "✅ Docker est installé"

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  Pensez à modifier .env selon vos besoins"
fi

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p workspace
mkdir -p agent/config

# Démarrer les services
echo "🐳 Démarrage des containers Docker..."
docker-compose up -d ollama

echo "⏳ Attente du démarrage d'Ollama (30 secondes)..."
sleep 30

# Télécharger le modèle par défaut
echo "📥 Téléchargement du modèle de code (qwen2.5-coder:7b)..."
echo "   Cela peut prendre plusieurs minutes selon votre connexion..."
docker-compose exec -T ollama ollama pull qwen2.5-coder:7b

echo ""
echo "✨ Installation terminée !"
echo ""
echo "Pour démarrer tous les services :"
echo "  ./scripts/start.sh"
echo ""
echo "Pour télécharger d'autres modèles :"
echo "  ./scripts/pull-model.sh <nom-du-modele>"
echo ""
echo "Modèles recommandés :"
echo "  - qwen2.5-coder:7b (déjà installé, optimal pour le code)"
echo "  - qwen2.5-coder:32b (plus puissant, nécessite plus de RAM)"
echo "  - deepseek-coder-v2:16b (excellent pour le code)"
echo "  - codellama:7b (spécialisé code)"
