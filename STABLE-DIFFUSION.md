# Stable Diffusion - Génération d'Images pour Claudine

Guide d'utilisation de Stable Diffusion intégré à Claudine pour la génération d'images (spritesheets, assets de jeux, illustrations).

## 🎯 Objectif

Permettre à l'agent WebUI de générer des images via Stable Diffusion, en complément de ses capacités de génération de code.

## 🚀 Démarrage Rapide

### 1. Démarrer le Service

```bash
# Démarrer tous les services (inclut Stable Diffusion)
make start

# Ou démarrer uniquement Stable Diffusion
docker-compose up -d stable-diffusion
```

### 2. Vérifier le Setup

```bash
# Vérifier que le service est prêt
make sd-setup

# Lister les modèles installés
make sd-models
```

### 3. Accéder à l'Interface

```bash
# Ouvrir l'interface web
make sd-ui

# Ou manuellement : http://localhost:7860
```

## 📦 Installation des Modèles

### Modèle de Base SD 1.5 (Recommandé pour démarrer)

```bash
# Via le script
make sd-download
# Choisir option 1

# Ou manuellement
docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors \
  https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors

# Redémarrer le service
docker-compose restart stable-diffusion
```

### SDXL (Meilleure Qualité)

```bash
# Télécharger SDXL (6.5 GB)
docker-compose exec stable-diffusion wget -O /data/models/Stable-diffusion/sd_xl_base_1.0.safetensors \
  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors
```

### LoRAs pour Game Assets

Pour des styles spécifiques (pixel art, sprites, etc.) :

1. Téléchargez depuis [Civitai](https://civitai.com)
2. Cherchez "pixel art lora" ou "sprite sheet lora"
3. Placez le fichier dans le volume :

```bash
# Copier un LoRA dans le conteneur
docker cp mon-lora.safetensors claudine-sd:/data/models/Lora/
docker-compose restart stable-diffusion
```

## 🎨 Utilisation

### Via l'Interface Web (Port 7860)

1. Ouvrez http://localhost:7860
2. Entrez votre prompt
3. Configurez les paramètres (steps, CFG scale, taille)
4. Cliquez "Generate"

### Via l'API REST

```bash
# Test simple
curl -X POST http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art character sprite, knight, 8 frames",
    "negative_prompt": "blurry, bad quality",
    "steps": 20,
    "width": 512,
    "height": 512
  }'
```

### Via l'Agent API (En Développement)

```bash
# Une fois l'intégration complète
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "2D game sprite sheet, character walking animation",
    "type": "spritesheet"
  }'
```

## 🎮 Cas d'Usage : Game Assets

### Générer un Spritesheet de Personnage

**Prompt** :
```
pixel art character sprite sheet, 8 frames walking animation,
knight with blue armor, side view, game asset, transparent background,
16x16 pixels per frame
```

**Paramètres** :
- Width: 512px (8 frames × 64px)
- Height: 64px
- Steps: 30
- CFG Scale: 7.5
- Sampler: DPM++ 2M Karras

### Générer des Item Icons

**Prompt** :
```
game item icons sprite sheet, potion bottles, swords, shields,
16x16 pixel art, RPG style, grid layout, transparent background
```

**Paramètres** :
- Width: 512px
- Height: 512px (grid 4×4)
- Steps: 25

### Générer un Background

**Prompt** :
```
pixel art game background, medieval castle, 2D platformer style,
parallax layer, seamless tileable
```

**Paramètres** :
- Width: 1024px
- Height: 512px
- Steps: 35

## ⚙️ Configuration

### Variables d'Environnement (.env)

```bash
# Activer Stable Diffusion
SD_ENABLED=true

# URL du service (interne Docker)
SD_API_URL=http://stable-diffusion:7860

# Port exposé
SD_PORT=7860

# Modèle par défaut
SD_DEFAULT_MODEL=v1-5-pruned-emaonly.safetensors

# Paramètres par défaut
SD_DEFAULT_STEPS=20
SD_DEFAULT_CFG_SCALE=7.0

# Sortie des images
IMAGE_OUTPUT_DIR=/workspace/generated-images
IMAGE_MAX_WIDTH=1024
IMAGE_MAX_HEIGHT=1024
```

### Activer le GPU NVIDIA

Dans `docker-compose.yml`, décommentez :

```yaml
stable-diffusion:
  # ...
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

Redémarrez :
```bash
docker-compose down
docker-compose up -d
```

## 🔧 Commandes Make

```bash
make sd-setup        # Setup et vérification
make sd-download     # Télécharger des modèles
make sd-models       # Lister modèles installés
make sd-logs         # Voir les logs
make sd-ui           # Ouvrir l'interface web
```

## 📊 Performance

### Sans GPU
- Temps de génération : 2-5 minutes par image (512×512)
- SDXL : 5-10 minutes
- Recommandé uniquement pour tests

### Avec GPU NVIDIA
- **RTX 3060** (12 GB) :
  - SD 1.5 : 5-10 secondes
  - SDXL : 15-20 secondes

- **RTX 4070+** (16 GB) :
  - SD 1.5 : 3-5 secondes
  - SDXL : 8-12 secondes

### VRAM Requise
- SD 1.5 : 4 GB minimum
- SDXL : 8 GB minimum
- Avec LoRAs : +1-2 GB par LoRA actif

## 🐛 Dépannage

### Le service ne démarre pas

```bash
# Vérifier les logs
make sd-logs

# Vérifier que le port n'est pas utilisé
lsof -i :7860

# Redémarrer le service
docker-compose restart stable-diffusion
```

### "CUDA out of memory"

Réduisez la taille de l'image ou utilisez `--no-half` dans les arguments CLI.

### L'API ne répond pas

```bash
# Attendre que le service soit complètement démarré (30-60 secondes)
curl http://localhost:7860/sdapi/v1/sd-models

# Vérifier le statut
docker-compose ps stable-diffusion
```

### Aucun modèle disponible

```bash
# Télécharger un modèle de base
make sd-download

# Vérifier les modèles
make sd-models
```

## 📚 Ressources

### Modèles
- [Hugging Face Models](https://huggingface.co/models?pipeline_tag=text-to-image)
- [Civitai](https://civitai.com) - Modèles communautaires et LoRAs
- [Stable Diffusion Models](https://rentry.org/sdmodels)

### Documentation
- [AUTOMATIC1111 Wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki)
- [API Documentation](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)

### Prompts pour Game Assets
- [Lexica.art](https://lexica.art) - Inspiration prompts
- [PromptHero](https://prompthero.com) - Prompts communautaires

## 🎯 Prochaines Étapes

- [x] Infrastructure Docker
- [x] Scripts de setup
- [x] Documentation
- [ ] Intégration API avec agent
- [ ] Endpoints `/generate-image` et `/generate-spritesheet`
- [ ] Intégration avec Open WebUI
- [ ] Prompts optimisés pour game assets
- [ ] Templates de génération

---

**Voir aussi** :
- [PHASE1-IMAGE-GENERATION.md](PHASE1-IMAGE-GENERATION.md) - Plan technique détaillé
- [ROADMAP.md](ROADMAP.md) - Roadmap complète du projet
