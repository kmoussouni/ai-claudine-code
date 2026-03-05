# Cahier de Recette - Phase 1 : Génération d'Images

Cahier de recette complet pour valider toutes les fonctionnalités de génération d'images.

## 📋 Informations Générales

- **Phase** : Phase 1 - Génération d'Images avec Stable Diffusion
- **Version** : 1.0.0
- **Date** : Décembre 2024
- **Environnement** : Serveur (192.168.1.12) + Client (Mac)

## 🎯 Objectifs de la Phase 1

- ✅ Intégrer Stable Diffusion dans l'infrastructure Docker
- ✅ Créer une API backend pour génération d'images
- ✅ Intégrer avec Open WebUI pour interface utilisateur
- ✅ Support spécifique game development (spritesheets, assets)

---

## 🧪 Tests Infrastructure

### TEST-INF-001 : Déploiement Docker

**Objectif** : Vérifier que tous les services démarrent correctement

**Prérequis** :
- Code à jour sur branche `feature/image-generation`
- Docker et Docker Compose installés

**Procédure** :
```bash
cd ~/ai/ai-claudine-code
git pull origin feature/image-generation
docker-compose down
docker-compose up -d
docker-compose ps
```

**Critères de Succès** :
- [ ] 4 conteneurs démarrés : `claudine-ollama`, `claudine-agent`, `claudine-webui`, `claudine-sd`
- [ ] Tous en état `Running` ou `Up`
- [ ] Aucune erreur dans les logs

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-INF-002 : Volumes Montés

**Objectif** : Vérifier que les volumes sont correctement montés

**Procédure** :
```bash
docker-compose exec webui ls -la /app/backend/data/functions/
docker-compose exec webui ls -la /app/backend/static/generated-images/
docker-compose exec code-agent ls -la /workspace/generated-images/
```

**Critères de Succès** :
- [ ] Dossier `/app/backend/data/functions/` contient les 3 fonctions .py
- [ ] Dossier `/workspace/generated-images/` existe et est accessible
- [ ] Permissions correctes (lecture/écriture)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-INF-003 : Connectivité Inter-Services

**Objectif** : Vérifier que les services peuvent communiquer

**Procédure** :
```bash
# Agent → Ollama
docker-compose exec code-agent curl http://ollama:11434/api/tags

# Agent → Stable Diffusion
docker-compose exec code-agent curl http://stable-diffusion:7860/sdapi/v1/sd-models

# WebUI → Agent
docker-compose exec webui curl http://code-agent:3000/health
```

**Critères de Succès** :
- [ ] Toutes les commandes retournent du JSON valide
- [ ] Pas d'erreur "Connection refused"
- [ ] Status codes 200 OK

**Résultat** : ☐ Réussi ☐ Échoué

---

## 🎨 Tests Stable Diffusion

### TEST-SD-001 : Service Démarrage

**Objectif** : Vérifier que Stable Diffusion démarre correctement

**Procédure** :
```bash
docker-compose logs stable-diffusion | tail -50
curl http://localhost:7860/sdapi/v1/sd-models
```

**Critères de Succès** :
- [ ] Logs montrent "Startup time: X.X seconds"
- [ ] Logs montrent "Running on http://0.0.0.0:7860"
- [ ] API répond avec liste de modèles (vide ou avec modèles)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-SD-002 : Installation Modèle

**Objectif** : Télécharger et installer le modèle SD 1.5

**Procédure** :
```bash
make sd-download
# Choisir option 1 (SD 1.5)
# Attendre téléchargement complet (~4 GB)
docker-compose restart stable-diffusion
sleep 30
make sd-models
```

**Critères de Succès** :
- [ ] Téléchargement réussi sans erreur
- [ ] Fichier `v1-5-pruned-emaonly.safetensors` présent
- [ ] Modèle listé après redémarrage

**Temps Estimé** : 5-10 minutes (selon connexion)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-SD-003 : Interface Web SD

**Objectif** : Tester l'interface Stable Diffusion directement

**Procédure** :
1. Ouvrir `http://localhost:7860` (ou `http://192.168.1.12:7860`)
2. Dans le champ prompt : `pixel art character, knight, game sprite`
3. Cliquer **Generate**
4. Attendre génération

**Critères de Succès** :
- [ ] Interface charge correctement
- [ ] Génération démarre (barre de progression)
- [ ] Image générée et affichée (10-30 secondes)
- [ ] Image de qualité correcte

**Résultat** : ☐ Réussi ☐ Échoué

---

## 🔌 Tests API Backend

### TEST-API-001 : Health Check SD

**Objectif** : Vérifier que l'agent peut communiquer avec SD

**Procédure** :
```bash
curl http://localhost:3000/sd/health | python3 -m json.tool
```

**Résultat Attendu** :
```json
{
  "status": "healthy",
  "url": "http://stable-diffusion:7860",
  "enabled": true
}
```

**Critères de Succès** :
- [ ] Status code 200
- [ ] `status` = "healthy"
- [ ] `enabled` = true

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-API-002 : Liste Modèles SD

**Objectif** : Vérifier que l'API peut lister les modèles SD

**Procédure** :
```bash
curl http://localhost:3000/sd/models | python3 -m json.tool
```

**Critères de Succès** :
- [ ] Status code 200
- [ ] JSON valide retourné
- [ ] Liste contient au moins le modèle SD 1.5

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-API-003 : Génération Image Simple

**Objectif** : Générer une image via l'API

**Procédure** :
```bash
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art character, knight with blue armor, game sprite",
    "width": 512,
    "height": 512,
    "steps": 20
  }' | python3 -m json.tool
```

**Critères de Succès** :
- [ ] Status code 200
- [ ] `status` = "success"
- [ ] `image_path` contient chemin valide
- [ ] `seed` est un nombre
- [ ] Temps génération < 30 secondes (avec GPU) ou < 5 minutes (CPU)

**Résultat** : ☐ Réussi ☐ Échoué

**Notes** :
- Seed généré : _______
- Chemin image : _______
- Temps génération : _______ secondes

---

### TEST-API-004 : Génération Spritesheet

**Objectif** : Générer un spritesheet multi-frames

**Procédure** :
```bash
curl -X POST http://localhost:3000/generate-spritesheet \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character walking animation, side view",
    "frames": 4,
    "frame_width": 64,
    "frame_height": 64,
    "steps": 30
  }' | python3 -m json.tool
```

**Critères de Succès** :
- [ ] Status code 200
- [ ] Image générée de taille 256x64 (4 frames × 64px)
- [ ] Prompt adapté visible (contient "sprite sheet", "frames")
- [ ] Fichier sauvegardé correctement

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-API-005 : Génération Game Asset

**Objectif** : Générer différents types d'assets de jeu

**Procédure** :

**Test 5a - Icon** :
```bash
curl -X POST http://localhost:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "icon",
    "description": "health potion, red liquid, glass bottle",
    "size": 256
  }' | python3 -m json.tool
```

**Test 5b - Item** :
```bash
curl -X POST http://localhost:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "item",
    "description": "magic sword with blue flames",
    "size": 512
  }' | python3 -m json.tool
```

**Critères de Succès** :
- [ ] Les deux requêtes retournent status "success"
- [ ] Prompts adaptés au type d'asset
- [ ] Images de tailles correctes (256x256, 512x512)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-API-006 : Validation Erreurs

**Objectif** : Vérifier la gestion d'erreurs

**Procédure** :

**Test 6a - Type Asset Invalide** :
```bash
curl -X POST http://localhost:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "invalid_type",
    "description": "test"
  }'
```

**Critères de Succès** :
- [ ] Status code 400 (Bad Request)
- [ ] Message d'erreur clair sur types valides

**Résultat** : ☐ Réussi ☐ Échoué

---

## 🖥️ Tests Interface WebUI

### TEST-UI-001 : Accès Interface

**Objectif** : Vérifier l'accès à Open WebUI

**Procédure** :
1. Ouvrir `http://localhost:8080` ou `http://192.168.1.12:8080`
2. Se connecter (créer compte si première fois)

**Critères de Succès** :
- [ ] Interface charge correctement
- [ ] Login/création compte fonctionne
- [ ] Accès au chat principal

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-UI-002 : Fonctions Disponibles

**Objectif** : Vérifier que les fonctions sont chargées

**Procédure** :
1. Cliquer sur profil → **Settings**
2. Aller dans **Functions**
3. Vérifier présence des fonctions

**Critères de Succès** :
- [ ] Fonction `Generate Image with Stable Diffusion` présente
- [ ] Fonction `Generate Spritesheet` présente
- [ ] Fonction `Generate Game Asset` présente
- [ ] Toutes activables (toggle switch)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-UI-003 : Activation Fonctions

**Objectif** : Activer les fonctions

**Procédure** :
1. Dans Settings → Functions
2. Activer chaque fonction (toggle ON)
3. Sauvegarder

**Critères de Succès** :
- [ ] Activation réussie sans erreur
- [ ] Fonctions restent activées après refresh
- [ ] Aucune erreur dans console navigateur

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-UI-004 : Génération Image via Chat

**Objectif** : Générer une image depuis le chat

**Procédure** :
1. Nouvelle conversation
2. Taper : `Peux-tu générer une image d'un chevalier en pixel art avec une armure bleue ?`
3. Envoyer
4. Attendre réponse

**Critères de Succès** :
- [ ] Agent comprend la demande
- [ ] Fonction `generate_image` est appelée
- [ ] Réponse formatée avec émojis et détails
- [ ] Chemin de l'image indiqué
- [ ] Seed affiché

**Résultat** : ☐ Réussi ☐ Échoué

**Capture** : (Screenshot de la réponse)

---

### TEST-UI-005 : Génération Spritesheet via Chat

**Objectif** : Générer un spritesheet depuis le chat

**Procédure** :
1. Dans le chat : `Crée-moi un spritesheet de marche pour un personnage, 8 frames, vue de côté`
2. Envoyer

**Critères de Succès** :
- [ ] Fonction `generate_spritesheet` appelée
- [ ] Réponse avec instructions Unity
- [ ] Détails frames (8 frames, 64x64)
- [ ] Dimensions totales correctes (512x64)

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-UI-006 : Génération Game Asset via Chat

**Objectif** : Générer un asset de jeu depuis le chat

**Procédure** :
1. Dans le chat : `Je veux une icône de potion de vie pour mon RPG, style pixel art`
2. Envoyer

**Critères de Succès** :
- [ ] Fonction `generate_game_asset` appelée
- [ ] Type détecté : "icon"
- [ ] Conseils d'utilisation affichés
- [ ] Image générée correctement

**Résultat** : ☐ Réussi ☐ Échoué

---

## 💾 Tests Sauvegarde Fichiers

### TEST-FILE-001 : Images Sauvegardées

**Objectif** : Vérifier que les images sont bien sauvegardées

**Procédure** :
```bash
ls -lh workspace/generated-images/
# Ou sur le serveur :
ls -lh ~/ai/ai-claudine-code/workspace/generated-images/
```

**Critères de Succès** :
- [ ] Au moins 3-4 fichiers PNG présents
- [ ] Nommage correct : `YYYYMMDD_HHMMSS_hash_seedXXXX.png`
- [ ] Tailles fichiers cohérentes (100KB - 2MB)
- [ ] Images visibles et valides

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-FILE-002 : Permissions Fichiers

**Objectif** : Vérifier les permissions

**Procédure** :
```bash
docker-compose exec code-agent ls -la /workspace/generated-images/
```

**Critères de Succès** :
- [ ] Fichiers lisibles et inscriptibles
- [ ] Pas de "Permission denied"

**Résultat** : ☐ Réussi ☐ Échoué

---

## 🎮 Tests Game Development

### TEST-GAME-001 : Workflow Complet Unity

**Objectif** : Créer assets pour un jeu Unity complet

**Procédure** :
Via le chat WebUI, générer :
1. Spritesheet personnage (8 frames marche)
2. Item épée magique
3. Icon potion de vie
4. Background château

**Critères de Succès** :
- [ ] 4 assets générés avec succès
- [ ] Style cohérent (pixel art)
- [ ] Tailles appropriées pour Unity
- [ ] Instructions Unity fournies

**Résultat** : ☐ Réussi ☐ Échoué

---

### TEST-GAME-002 : Import Unity (Optionnel)

**Objectif** : Tester l'import réel dans Unity

**Procédure** :
1. Copier images générées vers projet Unity
2. Importer spritesheet
3. Découper en frames
4. Créer animation

**Critères de Succès** :
- [ ] Import sans erreur
- [ ] Découpage frames correct
- [ ] Animation jouable

**Résultat** : ☐ Réussi ☐ Échoué ☐ Non testé

---

## ⚡ Tests Performance

### TEST-PERF-001 : Temps Génération (GPU)

**Objectif** : Mesurer performance avec GPU

**Prérequis** : GPU NVIDIA activé dans docker-compose.yml

**Procédure** :
Générer 3 images 512x512 avec 20 steps et mesurer :

**Critères de Succès** :
- [ ] Temps moyen < 15 secondes par image
- [ ] Pas d'erreur CUDA OOM
- [ ] GPU utilisé (vérifier dans logs SD)

**Résultats** :
- Image 1 : _____ secondes
- Image 2 : _____ secondes
- Image 3 : _____ secondes
- Moyenne : _____ secondes

**Résultat** : ☐ Réussi ☐ Échoué ☐ Non applicable

---

### TEST-PERF-002 : Temps Génération (CPU)

**Objectif** : Mesurer performance sans GPU

**Procédure** :
Même test que PERF-001 sans GPU

**Critères de Succès** :
- [ ] Temps < 5 minutes par image
- [ ] Pas de timeout
- [ ] Génération correcte

**Résultats** :
- Temps moyen : _____ minutes

**Résultat** : ☐ Réussi ☐ Échoué ☐ Non applicable

---

## 📊 Récapitulatif Final

### Statistiques Globales

- **Total tests** : 25
- **Tests réussis** : _____
- **Tests échoués** : _____
- **Tests non applicables** : _____
- **Taux de réussite** : _____%

### Validation Fonctionnalités Principales

| Fonctionnalité | Status | Notes |
|----------------|--------|-------|
| Infrastructure Docker | ☐ OK ☐ KO | |
| Stable Diffusion Setup | ☐ OK ☐ KO | |
| API Backend | ☐ OK ☐ KO | |
| Open WebUI Integration | ☐ OK ☐ KO | |
| Sauvegarde Fichiers | ☐ OK ☐ KO | |
| Performance | ☐ OK ☐ KO | |

### Blockers / Issues Identifiés

1. _____________________________________________________
2. _____________________________________________________
3. _____________________________________________________

### Recommandations

1. _____________________________________________________
2. _____________________________________________________
3. _____________________________________________________

---

## ✅ Validation Phase 1

**Phase 1 validée pour production** : ☐ OUI ☐ NON

**Signature** : _________________
**Date** : _________________

---

**Prochaines étapes** :
- [ ] Corriger issues identifiés
- [ ] Merger `feature/image-generation` dans `dev`
- [ ] Préparer Phase 2 (Génération Documents)
