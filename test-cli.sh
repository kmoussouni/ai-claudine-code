#!/bin/bash
# Test de l'agent CLI avec le modèle 7B

export OLLAMA_API_BASE="http://localhost:11434"
export DEFAULT_MODEL="qwen2.5-coder:7b"

echo "=== Test de Claudine Smart CLI ==="
echo ""
echo "Pour utiliser l'agent interactif, lancez :"
echo "  python3 scripts/claudine-smart.py"
echo ""
echo "Commandes disponibles :"
echo "  :help  - Aide"
echo "  :scan  - Scanner le projet"
echo "  :files - Lister les fichiers"
echo "  :model qwen2.5-coder:7b - Utiliser le modèle 7B"
echo "  :exit  - Quitter"
echo ""
echo "Exemples :"
echo '  "Explique ce qu'"'"'est ce projet"  - Discussion'
echo '  "Crée un fichier test.py"          - Modification (demande permission)'
echo ""
