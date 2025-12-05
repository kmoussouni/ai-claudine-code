# Claudine - Agent de Code Local

Agent de code intelligent utilisant des modèles AI open source hébergés localement. Alternative gratuite et open source à Claude Code et Codex, avec contrôle total de vos données et modèles.

## Caractéristiques

- 🤖 **100% Local** - Tous les modèles tournent sur votre machine
- 🔒 **Privé** - Vos données ne quittent jamais votre serveur
- 💰 **Gratuit** - Aucun coût d'API, entièrement open source
- 🐳 **Dockerisé** - Installation simple et portable
- 🚀 **Production-ready** - Prêt pour déploiement sur serveur
- 🔧 **Flexible** - Support de multiples modèles AI open source

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                      Claudine                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Web UI     │  │  Agent API   │  │   CLI Tool   │  │
│  │  Port 8080   │  │  Port 3000   │  │              │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │          │
│         └─────────────────┴─────────────────┘          │
│                           │                            │
│                    ┌──────▼──────┐                     │
│                    │   Ollama    │                     │
│                    │  Port 11434 │                     │
│                    │             │                     │
│                    │  Modèles:   │                     │
│                    │  - Qwen     │                     │
│                    │  - CodeLlama│                     │
│                    │  - DeepSeek │                     │
│                    └─────────────┘                     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Prérequis

- Docker & Docker Compose
- 16 GB RAM minimum (32 GB recommandé pour modèles plus grands)
- 20 GB d'espace disque libre
- (Optionnel) GPU NVIDIA avec CUDA pour performance accrue

## Installation Rapide

```bash
# 1. Cloner ou télécharger le projet
cd claudine

# 2. Configuration initiale (télécharge le modèle par défaut)
./scripts/setup.sh

# 3. Démarrer tous les services
./scripts/start.sh
```

C'est tout ! Les services sont maintenant accessibles :

- **API Agent** : http://localhost:3000
- **Web UI** : http://localhost:8080
- **Ollama API** : http://localhost:11434
- **Documentation API** : http://localhost:3000/docs

## Configuration

Copiez `.env.example` vers `.env` et ajustez selon vos besoins :

```bash
cp .env.example .env
```

Configuration disponible :

```env
# Modèle par défaut (voir section Modèles ci-dessous)
DEFAULT_MODEL=qwen2.5-coder:7b

# URL Ollama (garder par défaut pour Docker)
OLLAMA_BASE_URL=http://ollama:11434

# Ports des services
OLLAMA_PORT=11434
AGENT_PORT=3000
WEBUI_PORT=8080
```

## Modèles Disponibles

### Recommandés pour le Code

| Modèle | Taille | RAM requise | Description |
|--------|---------|-------------|-------------|
| `qwen2.5-coder:7b` | 4.7 GB | 8 GB | **Recommandé** - Excellent rapport performance/taille |
| `qwen2.5-coder:32b` | 19 GB | 32 GB | Très puissant pour code complexe |
| `deepseek-coder-v2:16b` | 9 GB | 16 GB | Excellent pour programmation |
| `codellama:7b` | 3.8 GB | 8 GB | Spécialisé Meta pour code |

### Usage Général

| Modèle | Taille | RAM requise | Description |
|--------|---------|-------------|-------------|
| `llama3.1:8b` | 4.7 GB | 8 GB | Polyvalent, très bon |
| `mistral:7b` | 4.1 GB | 8 GB | Rapide et efficace |

### Télécharger un Modèle

```bash
# Via script helper
./scripts/pull-model.sh qwen2.5-coder:32b

# Ou directement avec Docker
docker-compose exec ollama ollama pull deepseek-coder-v2:16b
```

## Utilisation

### 1. Interface Web (Recommandé pour débutants)

Ouvrez http://localhost:8080 dans votre navigateur.

- Interface intuitive type ChatGPT
- Support de fichiers
- Historique des conversations
- Prévisualisation code

### 2. CLI Python

```bash
# Vérifier l'état du système
python3 scripts/cli.py health

# Lister les modèles disponibles
python3 scripts/cli.py models

# Demander à l'agent de créer du code
python3 scripts/cli.py chat "Crée un serveur FastAPI avec endpoint /hello"

# Modifier un fichier existant
python3 scripts/cli.py chat "Ajoute la gestion d'erreurs" --files workspace/server.py

# Utiliser un modèle spécifique
python3 scripts/cli.py chat "Optimise cette fonction" \
  --files workspace/utils.py \
  --model qwen2.5-coder:32b

# Lister les fichiers du workspace
python3 scripts/cli.py files
```

### 3. Agents CLI Interactifs (Nouveau !)

Claudine propose **3 agents CLI** différents pour une expérience interactive comme Claude Code :

#### Agent Interactif (Recommandé pour débuter)
Session conversationnelle avec historique et gestion de contexte.

```bash
# Installer les dépendances
./scripts/install-cli-deps.sh

# Lancer l'agent
python3 scripts/agent-interactive.py
```

Commandes disponibles : `:help`, `:files`, `:model`, `:history`, `:workspace`, `:exit`

#### Agent Aider (Pour power users)
Utilise Aider directement pour des modifications de code puissantes.

```bash
./scripts/agent-aider.sh
```

Commandes disponibles : `/help`, `/add`, `/drop`, `/commit`, `/undo`, `/diff`

#### Agent TUI (Interface moderne)
Interface terminal avec vue splitée et boutons cliquables.

```bash
python3 scripts/agent-tui.py
```

**📖 Guide complet des 3 agents : [CLI-AGENTS.md](CLI-AGENTS.md)**

### 4. API REST

Documentation interactive : http://localhost:3000/docs

```bash
# Santé du système
curl http://localhost:3000/health

# Lister les modèles
curl http://localhost:3000/models

# Envoyer un message à l'agent
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Crée une fonction qui calcule fibonacci",
    "files": [],
    "model": "qwen2.5-coder:7b"
  }'
```

### 5. Intégration avec VS Code / IDEs

Utilisez l'extension **Continue** :

1. Installer l'extension Continue dans VS Code
2. Configurer `~/.continue/config.json` :

```json
{
  "models": [
    {
      "title": "Claudine Local",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b",
      "apiBase": "http://localhost:11434"
    }
  ]
}
```

## Workspace

Le répertoire `workspace/` est partagé avec les containers Docker. C'est là que l'agent travaille sur vos fichiers.

```bash
# Copier vos projets dans le workspace
cp -r mon-projet/ workspace/

# L'agent peut maintenant y accéder
python3 scripts/cli.py chat "Analyse le code dans workspace/mon-projet"
```

## Gestion des Services

```bash
# Démarrer tous les services
./scripts/start.sh

# Arrêter tous les services
./scripts/stop.sh

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f ollama
docker-compose logs -f code-agent

# Redémarrer un service
docker-compose restart code-agent

# État des containers
docker-compose ps
```

## Performance et Optimisation

### Avec CPU uniquement

Les modèles 7B tournent correctement sur CPU avec 16 GB RAM. Comptez :
- 10-30 secondes par réponse pour modèles 7B
- 30-60 secondes pour modèles 13-16B

### Avec GPU NVIDIA

Décommentez dans `docker-compose.yml` :

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

Performance attendue :
- 2-5 secondes par réponse pour 7B
- 5-10 secondes pour 32B

### Mac avec Apple Silicon (M1/M2/M3/M4)

Les modèles utilisent automatiquement l'accélération Metal. Très bonnes performances :
- Modèles 7B : 3-8 secondes par réponse
- Modèles 13B : 8-15 secondes

## Déploiement Serveur

### 1. Sur VPS / Serveur Linux

```bash
# Cloner le repo
git clone <votre-repo>
cd claudine

# Configuration
cp .env.example .env
# Éditez .env selon vos besoins

# Installation
./scripts/setup.sh

# Démarrer en mode daemon
./scripts/start.sh

# (Optionnel) Configurer comme service systemd
# Voir docs/systemd-service.md
```

### 2. Exposition publique (avec nginx)

```nginx
# /etc/nginx/sites-available/claudine
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

## Troubleshooting

### Le service Ollama ne démarre pas

```bash
# Vérifier les logs
docker-compose logs ollama

# Redémarrer
docker-compose restart ollama
```

### "Out of memory" lors du téléchargement de modèle

Utilisez un modèle plus petit (7B au lieu de 32B) ou augmentez la RAM.

### L'agent ne répond pas

```bash
# Vérifier que tous les services tournent
docker-compose ps

# Vérifier la santé
python3 scripts/cli.py health

# Redémarrer les services
./scripts/stop.sh && ./scripts/start.sh
```

### Performances lentes

- Utilisez un modèle plus petit (7B au lieu de 13B+)
- Activez le GPU si disponible
- Sur Mac M-series, vérifiez que Docker utilise bien l'architecture ARM

## Structure du Projet

```
claudine/
├── docker-compose.yml      # Orchestration des services
├── .env.example            # Configuration exemple
├── README.md               # Cette documentation
├── agent/                  # Service agent de code
│   ├── Dockerfile
│   ├── server.py           # API FastAPI
│   └── config/             # Configuration de l'agent
├── workspace/              # Espace de travail partagé
├── scripts/
│   ├── setup.sh            # Installation initiale
│   ├── start.sh            # Démarrer les services
│   ├── stop.sh             # Arrêter les services
│   ├── pull-model.sh       # Télécharger des modèles
│   └── cli.py              # Client CLI Python
└── .gitignore
```

## Technologies Utilisées

- **Ollama** - Runtime pour modèles LLM locaux
- **Aider** - Agent de code intelligent
- **FastAPI** - API REST moderne
- **Open WebUI** - Interface web pour LLMs
- **Docker** - Containerisation
- **Python** - Langage principal

## Contribuer

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -am 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## Licence

Ce projet est open source sous licence MIT.

## Ressources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Aider Documentation](https://aider.chat)
- [Continue.dev](https://continue.dev)
- [Open WebUI](https://github.com/open-webui/open-webui)

## Support

Pour toute question ou problème :
- Ouvrir une issue GitHub
- Consulter les logs avec `docker-compose logs`
- Vérifier la configuration dans `.env`

---

Développé avec ❤️ pour la communauté open source
