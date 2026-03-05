# Guide de Test - Phase 1 : Génération d'Images

Guide complet pour tester l'infrastructure de génération d'images sur le serveur et depuis le client.

## 🎯 Objectif

Valider que :
1. ✅ Stable Diffusion démarre correctement
2. ✅ Le modèle de base est installé
3. ✅ L'API de l'agent communique avec SD
4. ✅ Les endpoints de génération fonctionnent
5. ✅ Les images sont sauvegardées correctement

---

## 🖥️ PARTIE 1 : Tests sur le Serveur

### Étape 1 : Mise à Jour du Code

```bash
# Sur le serveur (192.168.1.12)
cd ~/ai/ai-claudine-code

# Récupérer les derniers changements
git pull origin feature/image-generation

# Vérifier qu'on est sur la bonne branche
git branch
git log --oneline -3
```

**Résultat attendu** :
```
* d8b5828 feat: Add image generation API endpoints and service
* 309b23c feat: Add Stable Diffusion infrastructure for image generation
* ed1ae56 docs: Add Phase 1 plan and complete roadmap for multimodal agent
```

### Étape 2 : Configuration

```bash
# Vérifier la configuration
cat .env | grep SD_

# Devrait afficher :
# SD_ENABLED=true
# SD_API_URL=http://stable-diffusion:7860
# SD_PORT=7860
# ...
```

### Étape 3 : Rebuild et Démarrage

```bash
# Rebuilder l'image de l'agent (inclut nouveaux services Python)
docker-compose build code-agent

# Démarrer TOUS les services
docker-compose up -d

# Vérifier que tout tourne
docker-compose ps
```

**Résultat attendu** :
```
claudine-ollama    Running
claudine-agent     Running
claudine-webui     Running
claudine-sd        Running (ou Starting si juste démarré)
```

### Étape 4 : Attendre que SD soit Prêt

```bash
# Stable Diffusion prend 30-60 secondes au premier démarrage
# Surveiller les logs
docker-compose logs -f stable-diffusion

# Attendre de voir :
# "Startup time: X.X seconds"
# "Running on http://0.0.0.0:7860"
```

**Ctrl+C** pour arrêter les logs une fois prêt.

### Étape 5 : Setup Stable Diffusion

```bash
# Vérifier que SD est accessible
make sd-setup

# Lister les modèles (devrait être vide au début)
make sd-models
```

**Résultat attendu** :
```
✅ API Stable Diffusion disponible !
📦 Modèles Stable Diffusion installés :
   ⚠️  Aucun modèle installé
```

### Étape 6 : Télécharger le Modèle SD 1.5

```bash
# Télécharger le modèle de base (4 GB)
make sd-download

# Choisir option 1 (SD 1.5)
# Puis confirmer avec 'o' ou 'y'

# Cela va prendre 5-10 minutes selon votre connexion
# Surveiller la progression
```

**Alternative manuelle** :
```bash
docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors \
  https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
```

### Étape 7 : Redémarrer SD

```bash
# Après téléchargement, redémarrer pour charger le modèle
docker-compose restart stable-diffusion

# Attendre 30 secondes
sleep 30

# Vérifier que le modèle est chargé
make sd-models
```

**Résultat attendu** :
```
📦 Modèles Stable Diffusion installés :
   - v1-5-pruned-emaonly.safetensors
```

### Étape 8 : Test Interface SD

```bash
# Ouvrir l'interface Stable Diffusion
make sd-ui

# Ou manuellement : http://localhost:7860
```

Dans l'interface :
1. Entrer un prompt simple : `pixel art character, knight`
2. Cliquer **Generate**
3. Vérifier qu'une image est générée (peut prendre 5-30 secondes)

**✅ Si ça fonctionne** : SD est opérationnel !

### Étape 9 : Test API Stable Diffusion (Direct)

```bash
# Test direct de l'API SD
curl http://localhost:7860/sdapi/v1/sd-models

# Devrait retourner du JSON avec le modèle
```

### Étape 10 : Test API Agent - Health Check

```bash
# Vérifier que l'agent peut communiquer avec SD
curl http://localhost:3000/sd/health

# Devrait retourner :
# {"status":"healthy","url":"http://stable-diffusion:7860","enabled":true}
```

**✅ Si ça fonctionne** : L'agent peut communiquer avec SD !

### Étape 11 : Test Génération d'Image via Agent API

```bash
# Test de génération simple
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art character, knight with blue armor, game sprite",
    "width": 512,
    "height": 512,
    "steps": 20
  }'

# Cela va prendre 10-30 secondes
# Devrait retourner du JSON avec :
# - status: "success"
# - image_path: "/workspace/generated-images/20250106_XXXXXX_XXXXXXXX_seedXXXX.png"
# - seed: numéro du seed utilisé
```

### Étape 12 : Vérifier l'Image Générée

```bash
# Lister les images générées
ls -lh /workspace/generated-images/

# Devrait afficher l'image PNG générée
```

**✅ SUCCESS** : L'infrastructure backend complète fonctionne !

---

## 💻 PARTIE 2 : Tests depuis le Client (Mac)

### Étape 1 : Test Health Check Distant

```bash
# Depuis votre Mac
curl http://192.168.1.12:3000/sd/health

# Devrait retourner :
# {"status":"healthy",...}
```

### Étape 2 : Lister les Modèles

```bash
curl http://192.168.1.12:3000/sd/models
```

### Étape 3 : Générer une Image Distante

```bash
curl -X POST http://192.168.1.12:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art knight character, blue armor, game sprite, 16-bit style",
    "negative_prompt": "blurry, 3d, realistic",
    "width": 512,
    "height": 512,
    "steps": 20,
    "cfg_scale": 7.5
  }' | python3 -m json.tool

# Devrait retourner le JSON formaté avec image_path
```

### Étape 4 : Test Génération Spritesheet

```bash
curl -X POST http://192.168.1.12:3000/generate-spritesheet \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character walking animation",
    "frames": 4,
    "frame_width": 64,
    "frame_height": 64,
    "steps": 30
  }' | python3 -m json.tool
```

### Étape 5 : Test Génération Game Asset

```bash
curl -X POST http://192.168.1.12:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "item",
    "description": "magic sword with blue flames",
    "size": 512,
    "steps": 25
  }' | python3 -m json.tool
```

### Étape 6 : Accès Interface Swagger

Ouvrir dans un navigateur sur le Mac :
```
http://192.168.1.12:3000/docs
```

Vous devriez voir la documentation Swagger interactive avec :
- Section "default" : Endpoints existants (chat, models, etc.)
- Section "Image Generation" : Nouveaux endpoints SD

Vous pouvez tester les endpoints directement depuis Swagger !

### Étape 7 : Accès Interface SD

```
http://192.168.1.12:7860
```

Tester la génération manuelle depuis l'interface.

---

## 🎨 PARTIE 3 : Tests Spécifiques Unity / Game Dev

### Test 1 : Spritesheet 8 Frames

```bash
curl -X POST http://192.168.1.12:3000/generate-spritesheet \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "knight character walking cycle animation, side view",
    "frames": 8,
    "frame_width": 64,
    "frame_height": 64,
    "steps": 35,
    "cfg_scale": 8.0
  }' -o spritesheet_test.json

# Extraire le chemin de l'image
cat spritesheet_test.json | grep image_path
```

### Test 2 : Icon Pack

```bash
curl -X POST http://192.168.1.12:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "icon",
    "description": "health potion, red liquid, glass bottle, RPG item icon",
    "size": 256,
    "steps": 20
  }'
```

### Test 3 : Tileset

```bash
curl -X POST http://192.168.1.12:3000/generate-game-asset \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "tileset",
    "description": "grass and stone tiles, medieval castle floor, seamless",
    "size": 512,
    "steps": 30
  }'
```

---

## 📊 Checklist de Validation

### Infrastructure
- [ ] Docker Compose démarre tous les services
- [ ] Stable Diffusion est accessible (port 7860)
- [ ] Agent API est accessible (port 3000)
- [ ] Modèle SD 1.5 est installé

### API Endpoints
- [ ] GET /sd/health retourne "healthy"
- [ ] GET /sd/models liste le modèle
- [ ] POST /generate-image génère une image
- [ ] POST /generate-spritesheet génère un spritesheet
- [ ] POST /generate-game-asset génère un asset

### Sauvegarde Fichiers
- [ ] Images sauvegardées dans /workspace/generated-images/
- [ ] Nommage correct (timestamp_hash_seed.png)
- [ ] Images visibles et valides (PNG)

### Performance
- [ ] Génération avec GPU : < 15 secondes
- [ ] Génération sans GPU : < 3 minutes
- [ ] Pas d'erreurs dans les logs

---

## 🐛 Dépannage

### SD ne démarre pas

```bash
# Vérifier les logs
docker-compose logs stable-diffusion

# Problèmes communs :
# - Port 7860 déjà utilisé
# - Manque de VRAM (si GPU)
# - Permission denied sur volumes
```

### API retourne 503 "SD n'est pas activé"

```bash
# Vérifier .env
cat .env | grep SD_ENABLED

# Rebuilder l'agent
docker-compose build code-agent
docker-compose restart code-agent
```

### Timeout lors de la génération

```bash
# Normal sans GPU (peut prendre 2-5 minutes)
# Avec GPU, vérifier :
docker-compose logs stable-diffusion | grep -i cuda
docker-compose logs stable-diffusion | grep -i gpu
```

### Images pas sauvegardées

```bash
# Vérifier les permissions
docker-compose exec code-agent ls -la /workspace/generated-images/

# Créer le dossier si absent
docker-compose exec code-agent mkdir -p /workspace/generated-images/
```

---

## ✅ Prochaines Étapes

Une fois tous les tests réussis :

1. **Documenter les résultats** (temps de génération, qualité, etc.)
2. **Optimiser les prompts** pour spritesheets Unity
3. **Intégrer avec Open WebUI** pour interface graphique
4. **Ajouter des LoRAs** pour meilleurs spritesheets pixel art

---

**Prêt à tester ?** Commencez par la Partie 1 sur le serveur !
