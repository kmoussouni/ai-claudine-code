# Claudine - Roadmap Agent Multimodal

## Vision Globale

Transformer Claudine en une plateforme multimodale complète avec deux agents spécialisés :

- **Agent WebUI** : Multimodal (images, vidéos, documents, code)
- **Agent CLI** : Spécialisé code (Node, JS, PHP, Symfony, Unity, C#, Python, Docker)

---

## Phase 0 : Infrastructure Client/Serveur (COMPLÉTÉE)

**Branche** : `fix/client-server` → mergée dans `dev`

### Réalisations
- [x] Configuration client/serveur propre
- [x] Documentation complète (REMOTE-SETUP.md)
- [x] Scripts d'installation améliorés
- [x] Makefile sans dépendances Python pour serveur
- [x] Modèle 32b configuré par défaut serveur

---

## Phase 1 : Génération d'Images avec FLUX (COMPLETEE)

**Branche** : `feature/image-generation` → merge vers `dev` pending
**Priorité** : HAUTE
**Durée estimée** : Complétée

### Objectifs
- ~~Intégrer Stable Diffusion pour génération d'images~~
- Intégrer FLUX pour génération d'images haute qualité
- Permettre création de spritesheets pour jeux (via prompts adaptés)
- Support assets de jeu (items, personnages, environnements)

### Décision Technologique : FLUX vs Stable Diffusion

Stable Diffusion / Automatic1111 a été **remplacé par FLUX/ComfyUI** pour les raisons suivantes :
- Qualité d'image supérieure (FLUX.1-schnell et FLUX.1-dev)
- Architecture moderne, meilleure cohérence des prompts
- ComfyUI expose une API workflow JSON flexible
- FLUX.1-schnell : license Apache 2.0, 4 steps (~5s GPU / plus lent CPU)
- Fonctionnement en **mode CPU** possible (pas de GPU NVIDIA requis)

### Technologies
- **FLUX/ComfyUI** (port 8188) — remplace Stable Diffusion/Automatic1111
- API REST via `agent/server.py` (FastAPI)
- Mode CPU forcé (GPU NVIDIA commenté dans docker-compose)
- Résolution native 1024x1024

### Livrables
- [x] Service FLUX/ComfyUI dans docker-compose
- [x] API endpoint `/generate-image` opérationnel
- [x] `agent/services/flux_generator.py` — client ComfyUI
- [x] Download validation + CPU mode forcé
- [x] Smart agent `claudine-smart.py` avec STACK_PRESETS (php, unity, js, react, bash, python)
- [x] Smart agent : `:commit`, `:review`, `:status`, `:stack` commands

### Note sur les Endpoints 501

`/generate-spritesheet` et `/generate-game-asset` retournent **501 intentionnellement**.
Utiliser `/generate-image` avec un prompt adapté :
```json
// Spritesheet
{ "prompt": "sprite sheet, 8 frames walking animation, knight, pixel art", "width": 1024, "height": 512, "steps": 4 }

// Game asset
{ "prompt": "game asset, icon, medieval sword, transparent background, pixel art", "width": 512, "height": 512 }
```

### Avancement

#### Infrastructure (COMPLÉTÉ)
- [x] Service FLUX/ComfyUI dans docker-compose
- [x] Migration complète de Stable Diffusion vers FLUX
- [x] Support CPU forcé avec validation téléchargement
- [x] Modèles FLUX.1-schnell et FLUX.1-dev configurés
- [x] Documentation migration (FLUX-MIGRATION.md)

#### Backend API (COMPLÉTÉ)
- [x] API endpoints `/generate-image` et `/generate-spritesheet`
- [x] Service image_generator.py avec support FLUX
- [x] CLI de génération d'images

#### Intégration WebUI (COMPLÉTÉ)
- [x] Intégration avec Open WebUI (fonctions pipeline)
- [x] Documentation Open WebUI (OPEN-WEBUI-SETUP.md)

#### Restant
- [ ] Tests end-to-end complets (GPU + CPU)
- [ ] Optimisation LoRAs pour game assets
- [ ] Merge vers `dev` après validation

**Détails** : Voir [PHASE1-IMAGE-GENERATION.md](PHASE1-IMAGE-GENERATION.md) et [FLUX-MIGRATION.md](FLUX-MIGRATION.md)

---

## Phase 2 : Génération de Documents

**Branche** : `feature/document-generation` (à créer)
**Priorité** : MOYENNE

### Objectifs
- Générer documents Word (.docx)
- Générer fichiers Excel (.xlsx)
- Support PDF avec mise en forme
- Templates personnalisables

### Technologies
- **python-docx** - Génération Word
- **openpyxl** - Génération Excel
- **reportlab** ou **weasyprint** - Génération PDF
- FastAPI endpoints dédiés

### Architecture
```
User request → LLM (génère contenu) → Python libs (créent fichiers)
              ↓
         Workspace/documents/
```

### Cas d'Usage
- Génération de rapports de projet
- Documentation technique automatique
- Feuilles de calcul avec données
- Game Design Documents (GDD)

### Livrables
- [ ] Service Python pour génération documents
- [ ] API endpoints `/generate-docx`, `/generate-xlsx`, `/generate-pdf`
- [ ] Templates de base (rapport, doc technique, GDD)
- [ ] Intégration WebUI
- [ ] Tests et documentation

---

## Phase 3 : Génération de Vidéos

**Branche** : `feature/video-generation` (à créer)
**Priorité** : BASSE (nice-to-have)

### Objectifs
- Génération vidéos courtes (animations, trailers)
- Animations de spritesheets
- Transitions et effets visuels

### Technologies

#### Option A : AnimateDiff + ComfyUI
- Génération vidéo à partir de prompts
- Contrôle précis avec workflows
- Support GPU NVIDIA

#### Option B : FFmpeg + Post-processing
- Assemblage d'images générées en vidéo
- Effets, transitions, audio
- Plus léger, moins de VRAM requise

### Cas d'Usage
- Animations de sprites pour jeux
- Trailers de jeu auto-générés
- Tutoriels vidéo animés
- GIFs animés pour UI

### Livrables
- [ ] Service ComfyUI ou FFmpeg dans docker-compose
- [ ] API endpoint `/generate-video`
- [ ] Workflows prédéfinis (animation sprite, trailer)
- [ ] Intégration WebUI
- [ ] Documentation

### Considérations
- VRAM élevée requise (12-16 GB pour AnimateDiff)
- Temps de génération long (2-10 min par vidéo)
- Peut être reportée si ressources limitées

---

## Phase 4 : Spécialisation Agent CLI

> **Note :** Partiellement réalisé en Phase 1 via les `STACK_PRESETS` de `claudine-smart.py` (php, unity, js, react, bash, python). Les prompts spécialisés par langage et la sélection de modèle par stack sont déjà fonctionnels.

**Branche** : `feature/cli-specialization` (à créer)
**Priorité** : MOYENNE

### Objectifs
- Optimiser agent CLI pour code uniquement
- Prompts spécialisés par langage/framework
- Performance et efficacité maximales

### Technologies
- Modèle optimisé (qwen2.5-coder:7b ou 14b)
- Prompts système personnalisés par langage
- Cache de contexte pour réponses rapides

### Spécialisations

#### Langages Backend
- **Node.js / Express** : APIs REST, microservices
- **PHP / Symfony** : Applications web, APIs
- **Python / FastAPI** : Services, ML/AI scripts

#### Langages Frontend
- **JavaScript / TypeScript** : Vanilla, modern ES6+
- **CSS / Sass** : Styling, responsive design
- **React / Vue** : Components, hooks, state

#### Game Development
- **Unity / C#** : Scripts, components, behaviors
- **Godot / GDScript** : 2D/3D game logic

#### DevOps
- **Docker** : Dockerfiles, docker-compose
- **Bash** : Scripts, automation
- **Git** : Workflows, hooks

### Livrables
- [ ] Prompts système par langage/framework
- [ ] Détection automatique contexte projet
- [ ] Scripts CLI améliorés avec modes spécialisés
- [ ] Benchmarks performance
- [ ] Documentation par langage

---

## Comparaison Agents Final

| Fonctionnalité | Agent WebUI | Agent CLI |
|----------------|-------------|-----------|
| **Génération code** | Oui | Oui (optimisé) |
| **Génération images** | Oui (FLUX) | Non |
| **Génération vidéos** | Oui | Non |
| **Génération documents** | Oui | Non |
| **Interface** | Web (port 8080) | CLI Python |
| **Modèle** | qwen2.5-coder:32b | qwen2.5-coder:7b |
| **RAM requise** | 20+ GB | 8-12 GB |
| **Cas d'usage** | Création assets, docs | Dev quotidien code |

---

## Timeline

```
Phase 0 : Client/Serveur              [COMPLÉTÉE]
             │
             ↓
Phase 1 : Images (FLUX/ComfyUI)       [COMPLETEE]
             │
             ↓
Phase 2 : Documents (docx/xlsx/pdf)   [À VENIR]
             │
             ↓
Phase 4 : CLI Spécialisé              [À VENIR]
             │
             ↓
Phase 3 : Vidéos (AnimateDiff)        [FUTUR - optionnel]
```

**Durée totale estimée** : 2-3 semaines restantes (Phase 1 complétée, Phase 4 partiellement faite)


---

## Prérequis Serveur

### Minimum (Phases 1-2-4)
- **CPU** : 8+ cores
- **RAM** : 32 GB
- **GPU** : NVIDIA RTX 3060 (12 GB VRAM) — *optionnel, FLUX fonctionne en mode CPU (plus lent)*
- **Stockage** : 100 GB SSD

### Recommandé (Toutes phases)
- **CPU** : 12+ cores
- **RAM** : 64 GB
- **GPU** : NVIDIA RTX 4070+ (16+ GB VRAM)
- **Stockage** : 200 GB NVMe SSD

---

## Workflow Git

1. Créer branche `feature/*` depuis `dev`
2. Développer et tester
3. Créer PR vers `dev`
4. Review et merge
5. Une fois toutes les phases testées : merge `dev` → `main`

---

**Prochaine action** : Merger `feature/image-generation` dans `dev`, puis commencer Phase 2
