#!/bin/bash
# Script helper pour exécuter les tests Phase 1
# Facilite l'exécution du cahier de recette

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

RESULTS_FILE="test-results-phase1.txt"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Tests Phase 1 - Génération d'Images               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📋 Ce script va exécuter les tests du cahier de recette"
echo "📝 Résultats sauvegardés dans : $RESULTS_FILE"
echo ""

# Initialiser fichier résultats
echo "=== Tests Phase 1 - Génération d'Images ===" > $RESULTS_FILE
echo "Date: $(date)" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE

# Fonction pour logger résultats
log_test() {
    local test_name=$1
    local status=$2
    local details=$3

    echo "" >> $RESULTS_FILE
    echo "[$test_name] $status" >> $RESULTS_FILE
    if [ ! -z "$details" ]; then
        echo "  Details: $details" >> $RESULTS_FILE
    fi

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $test_name${NC}"
    else
        echo -e "${RED}❌ $test_name${NC}"
    fi
}

# ==============================================================================
# TESTS INFRASTRUCTURE
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TESTS INFRASTRUCTURE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# TEST-INF-001: Déploiement Docker
echo "🔍 TEST-INF-001: Déploiement Docker..."
if docker-compose ps | grep -q "claudine-sd.*Running"; then
    log_test "TEST-INF-001" "PASS" "Tous les services running"
else
    log_test "TEST-INF-001" "FAIL" "Services manquants ou down"
fi

# TEST-INF-002: Volumes montés
echo "🔍 TEST-INF-002: Volumes montés..."
if docker-compose exec -T webui ls /app/backend/data/functions/ | grep -q "generate_image.py"; then
    log_test "TEST-INF-002" "PASS" "Fonctions WebUI montées"
else
    log_test "TEST-INF-002" "FAIL" "Fonctions WebUI non trouvées"
fi

# TEST-INF-003: Connectivité inter-services
echo "🔍 TEST-INF-003: Connectivité inter-services..."
if docker-compose exec -T code-agent curl -s http://ollama:11434/api/tags >/dev/null 2>&1; then
    log_test "TEST-INF-003" "PASS" "Agent → Ollama OK"
else
    log_test "TEST-INF-003" "FAIL" "Agent → Ollama KO"
fi

# ==============================================================================
# TESTS STABLE DIFFUSION
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TESTS STABLE DIFFUSION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# TEST-SD-001: Service démarré
echo "🔍 TEST-SD-001: Service Stable Diffusion..."
if curl -s http://localhost:7860/sdapi/v1/sd-models >/dev/null 2>&1; then
    log_test "TEST-SD-001" "PASS" "SD API accessible"
else
    log_test "TEST-SD-001" "FAIL" "SD API non accessible"
fi

# TEST-SD-002: Modèle installé
echo "🔍 TEST-SD-002: Modèle installé..."
if curl -s http://localhost:7860/sdapi/v1/sd-models | grep -q "v1-5"; then
    log_test "TEST-SD-002" "PASS" "Modèle SD 1.5 trouvé"
else
    log_test "TEST-SD-002" "WARN" "Aucun modèle trouvé - exécutez 'make sd-download'"
fi

# ==============================================================================
# TESTS API BACKEND
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TESTS API BACKEND${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# TEST-API-001: Health Check
echo "🔍 TEST-API-001: Health Check SD..."
health_response=$(curl -s http://localhost:3000/sd/health)
if echo "$health_response" | grep -q '"status":"healthy"'; then
    log_test "TEST-API-001" "PASS" "SD Health OK"
else
    log_test "TEST-API-001" "FAIL" "SD Health KO: $health_response"
fi

# TEST-API-002: Liste modèles
echo "🔍 TEST-API-002: Liste modèles SD..."
if curl -s http://localhost:3000/sd/models | grep -q "models"; then
    log_test "TEST-API-002" "PASS" "API liste modèles OK"
else
    log_test "TEST-API-002" "FAIL" "API liste modèles KO"
fi

# ==============================================================================
# TESTS FICHIERS
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  TESTS FICHIERS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# TEST-FILE-001: Dossier images
echo "🔍 TEST-FILE-001: Dossier images générées..."
if [ -d "workspace/generated-images" ]; then
    image_count=$(ls workspace/generated-images/*.png 2>/dev/null | wc -l)
    log_test "TEST-FILE-001" "PASS" "$image_count images trouvées"
else
    log_test "TEST-FILE-001" "FAIL" "Dossier generated-images absent"
fi

# ==============================================================================
# RÉSUMÉ
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  RÉSUMÉ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

total_tests=$(grep -c "TEST-" $RESULTS_FILE || echo "0")
passed_tests=$(grep -c "PASS" $RESULTS_FILE || echo "0")
failed_tests=$(grep -c "FAIL" $RESULTS_FILE || echo "0")
warn_tests=$(grep -c "WARN" $RESULTS_FILE || echo "0")

echo "📊 Tests exécutés : $total_tests"
echo -e "${GREEN}✅ Réussis : $passed_tests${NC}"
if [ "$failed_tests" -gt 0 ]; then
    echo -e "${RED}❌ Échoués : $failed_tests${NC}"
fi
if [ "$warn_tests" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Warnings : $warn_tests${NC}"
fi

echo ""
echo "📝 Résultats complets : $RESULTS_FILE"
echo ""

if [ "$failed_tests" -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✅ TOUS LES TESTS AUTOMATISÉS RÉUSSIS !                ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Prochaines étapes :"
    echo "  1. Tester l'interface WebUI manuellement"
    echo "  2. Générer quelques images de test"
    echo "  3. Consulter le cahier de recette complet (CAHIER-RECETTE-PHASE1.md)"
else
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║   ⚠️  CERTAINS TESTS ONT ÉCHOUÉ                          ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Consultez $RESULTS_FILE pour les détails"
    echo "Consultez les logs : docker-compose logs"
fi

echo ""
