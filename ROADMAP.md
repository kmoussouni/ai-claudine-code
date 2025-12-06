# Claudine - Roadmap Agent Multimodal

## 🎯 Vision Globale

Transformer Claudine en une plateforme multimodale complète avec deux agents spécialisés :

- **Agent WebUI** : Multimodal (images, vidéos, documents, code)
- **Agent CLI** : Spécialisé code (Node, JS, PHP, Symfony, Unity, C#, Python, Docker)

---

## ✅ Phase 0 : Infrastructure Client/Serveur (COMPLÉTÉE)

**Branche** : `fix/client-server` → mergée dans `dev`

### Réalisations
- ✅ Configuration client/serveur propre
- ✅ Documentation complète (REMOTE-SETUP.md)
- ✅ Scripts d'installation améliorés
- ✅ Makefile sans dépendances Python pour serveur
- ✅ Modèle 32b configuré par défaut serveur

---

## 🎨 Phase 1 : Génération d'Images (EN COURS)

**Branche** : `feature/image-generation`
**Priorité** : HAUTE
**Durée estimée** : 1-2 semaines

### Objectifs
- Intégrer Stable Diffusion pour génération d'images
- Permettre création de spritesheets pour jeux
- Support assets de jeu (items, personnages, environnements)

### Technologies
- Stable Diffusion WebUI (Automatic1111)
- API REST pour intégration
- LoRAs pour game assets et pixel art

### Livrables
- [ ] Service Stable Diffusion dans docker-compose
- [ ] API endpoints `/generate-image` et `/generate-spritesheet`
- [ ] Intégration avec Open WebUI
- [ ] Modèles de base + LoRAs game assets
- [ ] Documentation utilisateur

**Détails** : Voir [PHASE1-IMAGE-GENERATION.md](PHASE1-IMAGE-GENERATION.md)

---

## 📄 Phase 2 : Génération de Documents

**Branche** : `feature/document-generation` (à créer)
**Priorité** : MOYENNE
**Durée estimée** : 1 semaine

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

## 🎬 Phase 3 : Génération de Vidéos

**Branche** : `feature/video-generation` (à créer)
**Priorité** : BASSE (nice-to-have)
**Durée estimée** : 2-3 semaines

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

### Architecture
```
ComfyUI (port 8188) → API Workflows
    ↓
AnimateDiff models
    ↓
Vidéos générées → /workspace/videos/
```

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

### ⚠️ Considérations
- VRAM élevée requise (12-16 GB pour AnimateDiff)
- Temps de génération long (2-10 min par vidéo)
- Peut être reportée si ressources limitées

---

## 💻 Phase 4 : Spécialisation Agent CLI

**Branche** : `feature/cli-specialization` (à créer)
**Priorité** : MOYENNE
**Durée estimée** : 1 semaine

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

### Architecture
```
CLI Agent
  ├─→ Détection langage/framework
  ├─→ Chargement prompt spécialisé
  ├─→ Génération code optimisée
  └─→ Validation syntaxe (optionnel)
```

### Livrables
- [ ] Prompts système par langage/framework
- [ ] Détection automatique contexte projet
- [ ] Scripts CLI améliorés avec modes spécialisés
- [ ] Benchmarks performance
- [ ] Documentation par langage

### Exemple
```bash
# Détection automatique
claudine-smart "Add authentication to my Express API"
→ Détecte Node.js/Express → Charge prompt spécialisé

# Mode explicite
claudine-smart --mode symfony "Create CRUD for User entity"
→ Génère Symfony entities, controllers, forms
```

---

## 📊 Comparaison Agents Final

| Fonctionnalité | Agent WebUI | Agent CLI |
|----------------|-------------|-----------|
| **Génération code** | ✅ Oui | ✅ Oui (optimisé) |
| **Génération images** | ✅ Oui | ❌ Non |
| **Génération vidéos** | ✅ Oui | ❌ Non |
| **Génération documents** | ✅ Oui | ❌ Non |
| **Interface** | Web (port 8080) | CLI Python |
| **Modèle** | qwen2.5-coder:32b | qwen2.5-coder:7b |
| **RAM requise** | 20+ GB | 8-12 GB |
| **Cas d'usage** | Création assets, docs | Dev quotidien code |

---

## 🗓️ Timeline Proposée

```
┌─────────────────────────────────────────────────────────┐
│ Phase 0 : Client/Serveur              [✅ COMPLÉTÉE]    │
└─────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 1 : Images (Stable Diffusion)   [🔄 EN COURS]    │
│           1-2 semaines                                  │
└─────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 2 : Documents (docx/xlsx/pdf)   [⏳ À VENIR]     │
│           1 semaine                                     │
└─────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 4 : CLI Spécialisé              [⏳ À VENIR]     │
│           1 semaine                                     │
└─────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 3 : Vidéos (AnimateDiff)        [📅 FUTUR]       │
│           2-3 semaines (optionnel)                      │
└─────────────────────────────────────────────────────────┘
```

**Durée totale estimée** : 4-7 semaines (sans Phase 3 : 3-4 semaines)

---

## ⚙️ Prérequis Serveur

### Minimum (Phases 1-2-4)
- **CPU** : 8+ cores
- **RAM** : 32 GB
- **GPU** : NVIDIA RTX 3060 (12 GB VRAM)
- **Stockage** : 100 GB SSD

### Recommandé (Toutes phases)
- **CPU** : 12+ cores
- **RAM** : 64 GB
- **GPU** : NVIDIA RTX 4070+ (16+ GB VRAM)
- **Stockage** : 200 GB NVMe SSD

---

## 📝 Notes de Développement

### Workflow Git
1. Créer branche `feature/*` depuis `dev`
2. Développer et tester
3. Créer PR vers `dev`
4. Review et merge
5. Une fois toutes les phases testées : merge `dev` → `main`

### Tests Requis par Phase
- ✅ Tests unitaires (backend)
- ✅ Tests d'intégration (API)
- ✅ Tests end-to-end (UI → Backend → Service)
- ✅ Tests de performance (GPU, temps génération)

### Documentation Requise
- ✅ README phase
- ✅ API documentation (OpenAPI/Swagger)
- ✅ User guide avec exemples
- ✅ Troubleshooting section

---

**Prochaine action** : Commencer Phase 1 - Ajouter Stable Diffusion au docker-compose.yml
