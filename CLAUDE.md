# Claudine – Guide pour Claude Code

## Architecture des Services

| Service | Conteneur | Port | Description |
|---------|-----------|------|-------------|
| Ollama | `claudine-ollama` | 11434 | LLM local (modèles qwen2.5-coder) |
| Code Agent | `claudine-agent` | 3000 | FastAPI + Aider, édition de code |
| Open WebUI | `claudine-webui` | 8080 | Interface web multimodale |
| FLUX/ComfyUI | `claudine-flux` | 8188 | Génération d'images |

## Arborescence du Projet

```
ai-claudine-code/
├── agent/
│   ├── server.py              # FastAPI: endpoints chat, image, health
│   ├── Dockerfile
│   └── services/
│       └── flux_generator.py  # Client ComfyUI pour FLUX
├── flux-comfyui/
│   └── Dockerfile             # ComfyUI + modèles FLUX (CPU mode forcé)
├── scripts/
│   ├── claudine-smart.py      # Agent CLI hybride (PRÉFÉRÉ) — modifié non commité
│   ├── agent-interactive.py   # Agent CLI simple
│   ├── run-tests.sh           # Suite de tests (infra + API)
│   ├── setup.sh               # Première installation
│   └── install-cli-deps.sh    # Dépendances Python CLI
├── workspace/                 # Fichiers user + images générées (ne pas commiter)
├── webui-functions/           # Fonctions Open WebUI
├── docker-compose.yml         # Orchestration services
├── Makefile                   # Commandes make
├── .env.example               # Template variables d'env
├── ROADMAP.md                 # Phases du projet
└── AGENTS.md                  # (ancien guide — remplacé par ce fichier)
```

## Variables d'Environnement Clés

> **Gotcha critique :** Deux noms différents pour la même URL Ollama selon le contexte :
> - `OLLAMA_BASE_URL` → utilisé par `server.py` (FastAPI, conteneur)
> - `OLLAMA_API_BASE` → utilisé par Aider **et** par `claudine-smart.py` en CLI

| Variable | Défaut | Utilisé par |
|----------|--------|-------------|
| `OLLAMA_BASE_URL` | `http://ollama:11434` | `agent/server.py` |
| `OLLAMA_API_BASE` | `http://localhost:11434` | Aider, `claudine-smart.py` |
| `DEFAULT_MODEL` | `qwen2.5-coder:7b` | agent + CLI |
| `FLUX_ENABLED` | `true` | `server.py` |
| `FLUX_API_URL` | `http://flux-comfyui:8188` | `server.py` |
| `PHP_MODEL`, `JS_MODEL`, etc. | `DEFAULT_MODEL` | `claudine-smart.py` STACK_PRESETS |

## Commandes Build / Test / Dev

```bash
# Services Docker
make start          # Démarre tous les services
make stop           # Arrête tous les services
make status         # État des conteneurs
make logs           # Tail logs tous services
make build          # Rebuild images Docker
make setup          # Première installation complète

# Modèles
make pull MODEL=qwen2.5-coder:32b   # Télécharge un modèle Ollama

# Tests
./scripts/run-tests.sh   # Tests complets (infra + API) → test-results-phase1.txt
./test-cli.sh            # Smoke test CLI rapide

# CLI agents
python3 scripts/claudine-smart.py   # Agent hybride (PRÉFÉRÉ)
python3 scripts/agent-interactive.py  # Agent simple

# Client distant
make client-install
make remote-connect HOST=mon-serveur
```

## Commandes Claudine Smart (CLI)

```
:help          — Afficher l'aide
:scan          — Scanner le workspace
:files         — Lister les fichiers du workspace
:status        — git status condensé
:review        — Revue de code sur le diff courant
:commit <msg>  — git add -A && git commit -m <msg>
:auto [on/off] — Activer/désactiver auto-approve
:model <nom>   — Changer de modèle Ollama
:stack <nom>   — Preset langage (php, unity, js, react, bash, python)
:clear         — Effacer l'historique de session
:exit / :quit  — Quitter
```

## Endpoints API (`agent/server.py`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Info service |
| GET | `/health` | Santé API + Ollama |
| GET | `/models` | Modèles Ollama disponibles |
| POST | `/chat` | Chat avec Aider (édition fichiers) |
| POST | `/ollama/pull/{model}` | Télécharger un modèle |
| GET | `/workspace/files` | Lister fichiers workspace |
| GET | `/flux/health` | Santé FLUX/ComfyUI |
| GET | `/flux/models` | Modèles FLUX disponibles |
| POST | `/generate-image` | Générer image via FLUX ✅ |
| POST | `/generate-spritesheet` | **501** – utiliser `/generate-image` avec prompt adapté |
| POST | `/generate-game-asset` | **501** – utiliser `/generate-image` avec prompt adapté |

**Alternatives aux endpoints 501 :**
```json
// Spritesheet: POST /generate-image
{ "prompt": "sprite sheet, 8 frames walking animation, knight, pixel art", "width": 1024, "height": 512 }

// Game asset: POST /generate-image
{ "prompt": "game asset, icon, medieval sword, transparent background", "width": 512, "height": 512 }
```

## Conventions de Code

### Python
- PEP 8, indent 4 espaces, type hints où pratique
- Handlers FastAPI async, helpers dans `agent/services/`
- Env vars via `os.getenv()`, constantes en `UPPER_SNAKE_CASE`
- `pathlib.Path` plutôt que `os.path`

### Shell
- `set -euo pipefail` en tête de script
- Noms de fichiers en kebab-case
- Scripts idempotents (safe à relancer)

### Commits — Conventional Commits
```
feat: ajouter endpoint generate-video
fix: corriger timeout Aider sur gros fichiers
chore: mettre à jour dépendances Python
docs: documenter endpoints 501 dans CLAUDE.md
```

## Workflow Git

```
feature/* → dev → main
```

1. Créer branche `feature/<nom>` depuis `dev`
2. Développer et tester
3. PR vers `dev` (motivation + services impactés + tests)
4. Merger dans `main` quand `dev` est stable

**Branche actuelle :** `feature/image-generation` (claudine-smart.py non commité)

## Sécurité

- `.env` : **jamais commiter** — copier `.env.example`
- `workspace/` : scratch space, images générées — exclure du git
- Modèles AI et binaires lourds : ne pas commiter
- Ports non exposés publiquement ; utiliser SSH/VPN pour accès distant (`connect-remote.sh`)
- Secrets (WEBUI_SECRET_KEY) : stocker hors du repo

## Fichiers à Ne Jamais Commiter

```
.env
workspace/
workspace/generated-images/
.venv/
*.safetensors
*.ckpt
test-results-*.txt
```

## Checklist : Ajouter une Nouvelle Feature

- [ ] Créer branche `feature/<nom>` depuis `dev`
- [ ] Ajouter endpoint dans `agent/server.py` si API nécessaire
- [ ] Ajouter service dans `agent/services/` si logique complexe
- [ ] Mettre à jour `docker-compose.yml` si nouveau service Docker
- [ ] Étendre `scripts/run-tests.sh` avec tests couvrant la feature
- [ ] Mettre à jour `ROADMAP.md` (livrables cochés)
- [ ] Mettre à jour `README.md` ou docs pertinentes
- [ ] PR vers `dev` avec description complète
