#!/bin/bash
# Script de démarrage de Claudine

set -e

echo "🚀 Démarrage de Claudine..."

# Démarrer tous les services
docker-compose up -d

echo ""
echo "✅ Services démarrés !"
echo ""
echo "📍 URLs disponibles :"
echo "   - API Agent de code:  http://localhost:3000"
echo "   - Interface Web UI:   http://localhost:8080"
echo "   - Ollama API:         http://localhost:11434"
echo ""
echo "📖 Documentation API:    http://localhost:3000/docs"
echo ""
echo "Pour voir les logs :"
echo "  docker-compose logs -f"
echo ""
echo "Pour arrêter les services :"
echo "  ./scripts/stop.sh"
