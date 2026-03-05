# Roadmap — Claudine

Feuille de route du projet Claudine, agent de code local multi-modal.

> Dernière mise à jour : 2026-03-05

---

## Vue d'ensemble

| Phase | Fonctionnalité | Statut | Branche | Issues |
|-------|---------------|--------|---------|--------|
| 0 | Agent de code local + mode distant | Terminé | `main` | — |
| 1 | Génération d'images (FLUX) | Terminé | `feature/image-generation` | [#1][i1] [#2][i2] [#3][i3] |
| 2 | Génération de documents | Planifié | À créer | [#4][i4] |
| 3 | Génération de vidéos | Planifié | À créer | [#5][i5] |
| 4 | Spécialisation CLI par langage | Partiellement fait | À créer | [#6][i6] |

---

## Phase 0 — Agent de code local

Fondation du projet : agent de code utilisant des modèles AI open source (Ollama) avec interface Web, CLI et API REST.

**Livré :**
- Service agent FastAPI avec support Ollama (Qwen, CodeLlama, DeepSeek)
- Interface Web via Open WebUI
- 3 agents CLI (interactif, TUI, Aider)
- Mode client/serveur distant
- Docker Compose pour orchestration
- Intégration VS Code via Continue

---

## Phase 1 — Génération d'images (FLUX)

**Branche :** `feature/image-generation`
**Priorité :** HAUTE
**Statut :** Terminé

### Décision Technologique

Stable Diffusion / Automatic1111 a été **remplacé par FLUX/ComfyUI** :
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

### Complété
- [x] Migration complète de Stable Diffusion vers FLUX
- [x] Service FLUX/ComfyUI dans docker-compose
- [x] Support CPU forcé avec validation de téléchargement
- [x] Modèles FLUX.1-schnell (4 steps) et FLUX.1-dev (25 steps)
- [x] API endpoint `/generate-image` opérationnel
- [x] `agent/services/flux_generator.py` — client ComfyUI
- [x] CLI de génération d'images
- [x] Intégration avec Open WebUI (fonctions pipeline)
- [x] Smart agent `claudine-smart.py` avec STACK_PRESETS (php, unity, js, react, bash, python)
- [x] Smart agent : `:commit`, `:review`, `:status`, `:stack` commands
- [x] Documentation migration (FLUX-MIGRATION.md, OPEN-WEBUI-SETUP.md)

### Note sur les Endpoints 501

`/generate-spritesheet` et `/generate-game-asset` retournent **501 intentionnellement**.
Utiliser `/generate-image` avec un prompt adapté :
```json
// Spritesheet
{ "prompt": "sprite sheet, 8 frames walking animation, knight, pixel art", "width": 1024, "height": 512, "steps": 4 }

// Game asset
{ "prompt": "game asset, icon, medieval sword, transparent background, pixel art", "width": 512, "height": 512 }
```

### Restant
- [ ] Tests end-to-end complets GPU + CPU → [#2][i2]
- [ ] Optimisation LoRAs pour game assets (pixel art, sprites, tilesets) → [#3][i3]

**Détails** : Voir [PHASE1-IMAGE-GENERATION.md](PHASE1-IMAGE-GENERATION.md) et [FLUX-MIGRATION.md](FLUX-MIGRATION.md)

---

## Phase 2 — Génération de documents

**Branche :** `feature/document-generation` (à créer)
**Priorité :** MOYENNE

### Objectifs
- Génération Word (.docx) via python-docx
- Génération Excel (.xlsx) via openpyxl
- Génération PDF via reportlab/weasyprint
- Templates personnalisables (rapport, doc technique, GDD)

### Livrables
- [ ] Service Python pour génération de documents
- [ ] API endpoints `/generate-docx`, `/generate-xlsx`, `/generate-pdf`
- [ ] Templates de base
- [ ] Intégration WebUI
- [ ] Tests et documentation

> Détails : [#4][i4]

---

## Phase 3 — Génération de vidéos

**Branche :** `feature/video-generation` (à créer)
**Priorité :** BASSE

### Objectifs
- Génération de vidéos courtes (animations, trailers)
- Animations de spritesheets
- Transitions et effets visuels

### Options techniques
- **A) AnimateDiff + ComfyUI** — GPU requis (12-16 GB VRAM)
- **B) FFmpeg + post-processing** — plus léger, assemblage d'images

### Cas d'usage
- Animations de sprites pour jeux
- Trailers de jeu auto-générés
- GIFs animés pour UI

> Détails : [#5][i5]

---

## Phase 4 — Spécialisation CLI par langage

> **Note :** Partiellement réalisé en Phase 1 via les `STACK_PRESETS` de `claudine-smart.py` (php, unity, js, react, bash, python). Les prompts spécialisés par langage et la sélection de modèle par stack sont déjà fonctionnels.

**Branche :** `feature/cli-specialization` (à créer)
**Priorité :** MOYENNE

### Objectifs
- Prompts système spécialisés par langage/framework
- Détection automatique du contexte projet
- Cache de contexte pour réponses rapides

### Spécialisations prévues
- **Backend :** Node.js/Express, PHP/Symfony, Python/FastAPI
- **Frontend :** JavaScript/TypeScript, React/Vue
- **Game Dev :** Unity/C#, Godot/GDScript
- **DevOps :** Docker, Bash, Git

> Détails : [#6][i6]

---

## Comparaison Agents

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

**Prochaine action** : Finaliser merge des branches, puis commencer Phase 2

---

## Liens

[i1]: https://github.com/kmoussouni/ai-claudine-code/issues/1
[i2]: https://github.com/kmoussouni/ai-claudine-code/issues/2
[i3]: https://github.com/kmoussouni/ai-claudine-code/issues/3
[i4]: https://github.com/kmoussouni/ai-claudine-code/issues/4
[i5]: https://github.com/kmoussouni/ai-claudine-code/issues/5
[i6]: https://github.com/kmoussouni/ai-claudine-code/issues/6
