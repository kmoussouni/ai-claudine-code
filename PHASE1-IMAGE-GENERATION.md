# Phase 1 : Génération d'Images avec Stable Diffusion

## 🎯 Objectif

Permettre à l'agent WebUI de générer des images (spritesheets, assets de jeu, illustrations) via Stable Diffusion, tout en gardant l'agent CLI focalisé sur le code.

## 📐 Architecture Proposée

```
┌─────────────────────────────────────────────────┐
│  Open WebUI (port 8080)                         │
│  Interface utilisateur                          │
└────────────────┬────────────────────────────────┘
                 │
                 ├──→ Agent API (port 3000)
                 │    ├─→ /chat (texte/code via Ollama)
                 │    └─→ /generate-image (nouveau endpoint)
                 │              │
                 │              ↓
                 └──→ Stable Diffusion WebUI (port 7860)
                      - API REST pour génération d'images
                      - Modèles: SD 1.5, SDXL, LoRAs pour game assets
```

## 🛠️ Composants à Ajouter

### 1. Service Stable Diffusion (Docker)

**Choix du service** : Automatic1111 Stable Diffusion WebUI
- ✅ Mature et stable
- ✅ API REST complète
- ✅ Support GPU NVIDIA
- ✅ Large communauté et modèles disponibles
- ✅ Interface web incluse pour debug

**Alternative** : ComfyUI (plus moderne mais plus complexe)

### 2. Intégration dans docker-compose.yml

```yaml
services:
  # ... services existants ...

  stable-diffusion:
    image: ghcr.io/AbdBarho/stable-diffusion-webui:latest
    container_name: claudine-sd
    ports:
      - "7860:7860"
    volumes:
      - sd_models:/data/models
      - sd_outputs:/outputs
    environment:
      - CLI_ARGS=--api --listen --port 7860
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  sd_models:
  sd_outputs:
```

### 3. Nouveau Service API Python

Créer `agent/services/image_generator.py` :

```python
import httpx
import base64
from typing import Optional, Dict, Any

class ImageGenerator:
    def __init__(self, sd_url: str = "http://stable-diffusion:7860"):
        self.sd_url = sd_url
        self.client = httpx.AsyncClient(timeout=300.0)

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        cfg_scale: float = 7.0,
        seed: int = -1
    ) -> Dict[str, Any]:
        """Génère une image via Stable Diffusion API"""

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt or "blurry, bad quality, distorted",
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed,
            "sampler_name": "DPM++ 2M Karras",
        }

        response = await self.client.post(
            f"{self.sd_url}/sdapi/v1/txt2img",
            json=payload
        )

        result = response.json()

        # L'image est en base64 dans result['images'][0]
        return {
            "image": result['images'][0],
            "info": result.get('info', {})
        }

    async def generate_spritesheet(
        self,
        prompt: str,
        frames: int = 4,
        **kwargs
    ) -> Dict[str, Any]:
        """Génère un spritesheet pour jeu vidéo"""

        # Adapter le prompt pour spritesheet
        spritesheet_prompt = f"{prompt}, sprite sheet, multiple frames, {frames} frames, game asset, pixel art style"

        return await self.generate_image(
            prompt=spritesheet_prompt,
            width=512,
            height=128,  # Format spritesheet
            **kwargs
        )
```

### 4. Nouveaux Endpoints API

Dans `agent/main.py` (FastAPI) :

```python
from services.image_generator import ImageGenerator

image_gen = ImageGenerator()

@app.post("/generate-image")
async def generate_image(request: ImageGenerationRequest):
    """Endpoint pour génération d'images"""

    result = await image_gen.generate_image(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        width=request.width,
        height=request.height,
        steps=request.steps,
        cfg_scale=request.cfg_scale,
        seed=request.seed
    )

    # Sauvegarder l'image dans /workspace/generated-images/
    image_path = save_image(result['image'], request.prompt)

    return {
        "status": "success",
        "image_url": f"/outputs/{image_path}",
        "image_base64": result['image'],
        "info": result['info']
    }

@app.post("/generate-spritesheet")
async def generate_spritesheet(request: SpritesheetRequest):
    """Endpoint spécialisé pour spritesheets de jeux"""

    result = await image_gen.generate_spritesheet(
        prompt=request.prompt,
        frames=request.frames,
        negative_prompt=request.negative_prompt
    )

    return {
        "status": "success",
        "spritesheet_url": f"/outputs/{image_path}",
        "frames": request.frames
    }
```

### 5. Intégration avec Open WebUI

**Option A** : Via Plugin/Extension Open WebUI
- Créer un plugin custom pour Open WebUI qui détecte les requêtes d'images
- Rediriger vers l'endpoint `/generate-image`

**Option B** : Via Prompt Engineering
- L'agent détecte automatiquement quand l'utilisateur demande une image
- Génère un appel API en interne
- Retourne l'image dans la conversation

**Option C** : Bouton dédié dans l'UI
- Ajouter un bouton "Generate Image" dans Open WebUI
- Modal pour paramètres (prompt, taille, etc.)

## 📦 Modèles à Installer

### Pour Démarrer
- **Stable Diffusion 1.5** (4 GB) - Rapide, bon pour tests
- **SDXL** (6.5 GB) - Qualité supérieure

### Pour Game Assets / Spritesheets
- **LoRA Pixel Art** - Style pixel art pour jeux rétro
- **LoRA Sprite Sheet** - Optimisé pour spritesheets
- **ControlNet** - Pour contrôle précis des poses

## 🔧 Variables d'Environnement

Ajouter dans `.env` :

```bash
# Stable Diffusion
SD_ENABLED=true
SD_API_URL=http://stable-diffusion:7860
SD_DEFAULT_MODEL=v1-5-pruned-emaonly.safetensors
SD_GPU_ENABLED=true

# Génération d'images
IMAGE_OUTPUT_DIR=/workspace/generated-images
IMAGE_MAX_SIZE=1024
IMAGE_DEFAULT_STEPS=20
```

## 📝 Plan d'Implémentation

### Étape 1 : Infrastructure
- [ ] Ajouter service Stable Diffusion au docker-compose.yml
- [ ] Créer volumes pour modèles et outputs
- [ ] Télécharger modèle de base SD 1.5
- [ ] Tester accès API Stable Diffusion

### Étape 2 : Backend
- [ ] Créer `agent/services/image_generator.py`
- [ ] Ajouter endpoints FastAPI pour génération
- [ ] Créer dossier workspace/generated-images
- [ ] Tests unitaires pour l'API

### Étape 3 : Intégration WebUI
- [ ] Configurer Open WebUI pour détecter requêtes images
- [ ] Créer interface pour paramètres (optionnel)
- [ ] Tester workflow complet

### Étape 4 : Optimisation
- [ ] Installer LoRAs pour game assets
- [ ] Fine-tuning des prompts pour spritesheets
- [ ] Cache des modèles en mémoire
- [ ] Documentation utilisateur

## 🎮 Cas d'Usage : Spritesheets pour Unity

### Exemple 1 : Character Sprite
```
Prompt: "2D pixel art character sprite sheet, 8 frames walking animation,
knight with blue armor, side view, game asset, transparent background"

Paramètres:
- Width: 512px
- Height: 64px (8 frames de 64x64)
- Steps: 30
- CFG Scale: 7.5
```

### Exemple 2 : Item Icons
```
Prompt: "game item icons, potion bottles, sword, shield, 16x16 pixel art,
multiple items, sprite sheet, RPG style"

Paramètres:
- Width: 512px
- Height: 512px (grid 4x4 d'items)
- Steps: 25
```

## ⚠️ Considérations

### Performance
- GPU NVIDIA recommandée (RTX 3060+ pour SDXL)
- Sans GPU : temps de génération ~2-5 min par image
- Avec GPU : ~5-10 secondes par image

### Mémoire
- SD 1.5 : ~4 GB VRAM
- SDXL : ~8 GB VRAM minimum
- Avec autres services : prévoir 12-16 GB VRAM total

### Stockage
- Modèles : 5-20 GB
- Images générées : prévoir 1-2 GB par 1000 images

## 📚 Ressources

- [Automatic1111 API Docs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
- [Civitai Models](https://civitai.com/) - Modèles et LoRAs communautaires
- [ControlNet](https://github.com/Mikubill/sd-webui-controlnet) - Contrôle précis

---

**Prochaines étapes** : Commencer par l'Étape 1 - Infrastructure
