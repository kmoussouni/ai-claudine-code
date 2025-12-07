# Modèles Stable Diffusion

Ce projet supporte 2 modèles de génération d'images :

## 📦 Modèles disponibles

### 1. SD v1.5 (par défaut)
- **Nom** : `v1-5-pruned-emaonly`
- **Taille** : 4 GB
- **Vitesse** : Rapide
- **Qualité** : Correcte
- **Usage** : Tests rapides, prototypage

### 2. SDXL Base
- **Nom** : `sd_xl_base_1.0`
- **Taille** : 7 GB
- **Vitesse** : Plus lent
- **Qualité** : Excellente
- **Usage** : Production, haute qualité

## 🚀 Utilisation

### Via l'API REST

**Utiliser SD v1.5 (par défaut)** :
```bash
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art knight with blue armor",
    "width": 512,
    "height": 512
  }'
```

**Utiliser SDXL** :
```bash
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art knight with blue armor",
    "width": 1024,
    "height": 1024,
    "model_name": "sd_xl_base_1.0"
  }'
```

### Via Open WebUI

Les fonctions supportent automatiquement le paramètre `model_name`.

## ⚙️ Configuration recommandée

### Pour SD v1.5
- **Résolution** : 512x512
- **Steps** : 20-30
- **CFG Scale** : 7.0

### Pour SDXL
- **Résolution** : 1024x1024 (natif)
- **Steps** : 25-40
- **CFG Scale** : 7.0-8.0

## 💾 Téléchargement des modèles

Au premier démarrage de Stable Diffusion, les modèles sont automatiquement téléchargés :
- SD v1.5 : ~4 GB
- SDXL : ~7 GB

**Total** : ~11 GB d'espace disque requis

## 🖥️ Ressources requises

### SD v1.5 (CPU)
- RAM : 8 GB minimum
- Temps : ~10-15s par image

### SDXL (CPU)
- RAM : 16 GB minimum
- Temps : ~30-60s par image

### Avec GPU (CUDA)
- SD v1.5 : ~2-3s par image
- SDXL : ~5-10s par image

## 🔧 Changer le modèle par défaut

Modifier dans `agent/services/image_generator.py` :

```python
# Par défaut SDXL
async def generate_image(
    self,
    prompt: str,
    model_name: Optional[str] = "sd_xl_base_1.0"  # Changer ici
    ...
)
```
