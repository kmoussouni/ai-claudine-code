# Roadmap — Claudine

Feuille de route du projet Claudine, agent de code local multi-modal.

> Dernière mise à jour : 2026-02-21

---

## Vue d'ensemble

| Phase | Fonctionnalité | Statut | Branche | Issues |
|-------|---------------|--------|---------|--------|
| 0 | Agent de code local + mode distant | ✅ Terminé | `main` | — |
| 1 | Génération d'images (FLUX) | 🔧 En cours (~90%) | `feature/image-generation` | [#1][i1] [#2][i2] [#3][i3] |
| 2 | Génération de documents | 📋 Planifié | À créer | [#4][i4] |
| 3 | Génération de vidéos | 📋 Planifié | À créer | [#5][i5] |
| 4 | Spécialisation CLI par langage | 📋 Planifié | À créer | [#6][i6] |

---

## Phase 0 — Agent de code local ✅

Fondation du projet : agent de code utilisant des modèles AI open source (Ollama) avec interface Web, CLI et API REST.

**Livré :**
- Service agent FastAPI avec support Ollama (Qwen, CodeLlama, DeepSeek)
- Interface Web via Open WebUI
- 3 agents CLI (interactif, TUI, Aider)
- Mode client/serveur distant
- Docker Compose pour orchestration
- Intégration VS Code via Continue

---

## Phase 1 — Génération d'images (FLUX) 🔧

**Branche :** `feature/image-generation`
**Priorité :** HAUTE

### Complété ✅
- Migration complète de Stable Diffusion vers FLUX
- Service FLUX/ComfyUI dans docker-compose
- Support CPU forcé avec validation de téléchargement
- Modèles FLUX.1-schnell (4 steps) et FLUX.1-dev (25 steps)
- API endpoints `/generate-image` et `/generate-spritesheet`
- Service `image_generator.py` avec support FLUX
- CLI de génération d'images
- Intégration avec Open WebUI
- Documentation migration

### Restant 🔲
- Tests end-to-end complets GPU + CPU → [#2][i2]
- Optimisation LoRAs pour game assets (pixel art, sprites, tilesets) → [#3][i3]
- Merge vers `dev` après validation → [#1][i1]

---

## Phase 2 — Génération de documents 📋

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

→ Détails : [#4][i4]

---

## Phase 3 — Génération de vidéos 📋

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

→ Détails : [#5][i5]

---

## Phase 4 — Spécialisation CLI par langage 📋

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

→ Détails : [#6][i6]

---

## Liens

[i1]: https://github.com/kmoussouni/ai-claudine-code/issues/1
[i2]: https://github.com/kmoussouni/ai-claudine-code/issues/2
[i3]: https://github.com/kmoussouni/ai-claudine-code/issues/3
[i4]: https://github.com/kmoussouni/ai-claudine-code/issues/4
[i5]: https://github.com/kmoussouni/ai-claudine-code/issues/5
[i6]: https://github.com/kmoussouni/ai-claudine-code/issues/6
