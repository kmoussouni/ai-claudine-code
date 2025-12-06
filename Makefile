.PHONY: help setup start stop restart logs status models pull clean client-install remote-connect remote-disconnect remote-status

help: ## Afficher cette aide
	@echo "Claudine - Agent de Code Local"
	@echo "================================"
	@echo ""
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Installation et configuration initiale
	@./scripts/setup.sh

start: ## Démarrer tous les services
	@./scripts/start.sh

stop: ## Arrêter tous les services
	@./scripts/stop.sh

restart: stop start ## Redémarrer tous les services

logs: ## Afficher les logs de tous les services
	@docker-compose logs -f

status: ## Afficher l'état des services
	@docker-compose ps
	@echo ""
	@echo "🏥 État de santé du système :"
	@curl -s http://localhost:3000/health 2>/dev/null | grep -q "api" && echo "   API: ✅ OK" || echo "   API: ❌ Erreur"
	@curl -s http://localhost:11434/api/tags 2>/dev/null >/dev/null && echo "   Ollama: ✅ OK" || echo "   Ollama: ❌ Erreur"

models: ## Lister les modèles disponibles
	@echo "📦 Modèles disponibles :"
	@docker-compose exec -T ollama ollama list

pull: ## Télécharger un modèle (usage: make pull MODEL=qwen2.5-coder:32b)
	@./scripts/pull-model.sh $(MODEL)

clean: ## Nettoyer les volumes Docker (ATTENTION: supprime les données)
	@echo "⚠️  ATTENTION: Ceci va supprimer tous les volumes Docker et données"
	@read -p "Êtes-vous sûr? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "✅ Nettoyage terminé"; \
	else \
		echo "❌ Annulé"; \
	fi

dev-logs-ollama: ## Logs uniquement Ollama
	@docker-compose logs -f ollama

dev-logs-agent: ## Logs uniquement Agent
	@docker-compose logs -f code-agent

dev-logs-webui: ## Logs uniquement WebUI
	@docker-compose logs -f webui

build: ## Rebuilder les images Docker
	@docker-compose build --no-cache

# Commandes Client/Serveur
client-install: ## Installer le client léger (sans Docker)
	@./scripts/install-client.sh

remote-connect: ## Se connecter au serveur distant (usage: make remote-connect HOST=monserveur.com)
	@./scripts/connect-remote.sh start --host $(HOST)

remote-disconnect: ## Déconnecter du serveur distant
	@./scripts/connect-remote.sh stop

remote-status: ## Status de la connexion distante
	@./scripts/connect-remote.sh status
