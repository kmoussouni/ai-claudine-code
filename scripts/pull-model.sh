#!/bin/bash
# Script pour télécharger de nouveaux modèles

if [ -z "$1" ]; then
    echo "Usage: $0 <nom-du-modele>"
    echo ""
    echo "Exemples de modèles populaires :"
    echo "  - qwen2.5-coder:7b       (optimal pour code, 4.7GB)"
    echo "  - qwen2.5-coder:32b      (très puissant, 19GB)"
    echo "  - deepseek-coder-v2:16b  (excellent pour code, 9GB)"
    echo "  - codellama:7b           (spécialisé code, 3.8GB)"
    echo "  - llama3.1:8b            (usage général, 4.7GB)"
    echo "  - mistral:7b             (usage général, 4.1GB)"
    exit 1
fi

MODEL=$1

echo "📥 Téléchargement du modèle: $MODEL"
echo "   Cela peut prendre plusieurs minutes..."

docker-compose exec ollama ollama pull "$MODEL"

echo ""
echo "✅ Modèle $MODEL téléchargé avec succès !"
echo ""
echo "Pour l'utiliser, modifiez DEFAULT_MODEL dans .env :"
echo "  DEFAULT_MODEL=$MODEL"
