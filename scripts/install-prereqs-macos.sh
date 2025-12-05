#!/bin/bash
# Script d'installation des prérequis pour macOS

set -e

echo "🍎 Installation des prérequis pour Claudine sur macOS"
echo "======================================================"

# Vérifier si Homebrew est installé
if ! command -v brew &> /dev/null; then
    echo "📦 Installation de Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew déjà installé"
fi

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo ""
    echo "🐳 Docker n'est pas installé"
    echo "   Veuillez installer Docker Desktop depuis:"
    echo "   https://www.docker.com/products/docker-desktop"
    echo ""
    echo "   Ou avec Homebrew:"
    echo "   brew install --cask docker"
    echo ""
    read -p "Appuyez sur Entrée quand Docker est installé..."
else
    echo "✅ Docker déjà installé"
fi

# Vérifier si Python 3 est installé
if ! command -v python3 &> /dev/null; then
    echo "🐍 Installation de Python 3..."
    brew install python3
else
    echo "✅ Python 3 déjà installé ($(python3 --version))"
fi

# Installer les dépendances Python pour le CLI
echo "📚 Installation des dépendances Python..."
pip3 install --user httpx

echo ""
echo "✅ Tous les prérequis sont installés !"
echo ""
echo "Prochaines étapes :"
echo "  1. Assurez-vous que Docker Desktop est démarré"
echo "  2. Lancez: ./scripts/setup.sh"
