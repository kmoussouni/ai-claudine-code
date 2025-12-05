#!/bin/bash
# Script d'installation des dépendances pour les Agents CLI

set -e

echo "📦 Installation des dépendances pour les Agents CLI Claudine"
echo "============================================================="

# Vérifier que Python 3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "   Sur macOS: brew install python3"
    exit 1
fi

echo "✅ Python 3 trouvé: $(python3 --version)"

# Vérifier que pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé"
    exit 1
fi

echo ""
echo "Installation des dépendances..."
echo ""

# Installer les dépendances
pip3 install -r requirements-cli.txt

echo ""
echo "✅ Installation terminée !"
echo ""
echo "Agents CLI disponibles:"
echo "  1. Agent Interactif : python3 scripts/agent-interactive.py"
echo "  2. Agent Aider      : ./scripts/agent-aider.sh"
echo "  3. Agent TUI        : python3 scripts/agent-tui.py"
echo ""
echo "Pour plus d'informations, consultez: CLI-AGENTS.md"
