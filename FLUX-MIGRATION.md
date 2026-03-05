# Migration Stable Diffusion → FLUX

## 🎯 Pourquoi FLUX ?

| Critère | Stable Diffusion v1.5 | SDXL | **FLUX.1** |
|---------|----------------------|------|---------|
| Qualité | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Vitesse (GPU) | Rapide | Moyen | Très rapide |
| Compréhension prompts | Basique | Bon | Excellent |
| Texte dans images | ❌ Mauvais | ⚠️ Moyen | ✅ Excellent |
| Résolution native | 512x512 | 1024x1024 | 1024x1024 |

## 📦 Modèles FLUX

### FLUX.1-schnell (Recommandé)
- **Vitesse** : 4 steps (~3-5s sur GPU)
- **Taille** : 12 GB
- **Licence** : Apache 2.0 (usage commercial OK)
- **Usage** : Production, rapide

### FLUX.1-dev
- **Qualité** : Maximale, 20-30 steps
- **Taille** : 12 GB
- **Licence** : Non-commercial uniquement
- **Usage** : Tests, haute qualité

## 🔄 Changements

### Avant (Stable Diffusion)
```bash
docker-compose up -d
# Port 7860 - SD WebUI
# API: http://localhost:3000/generate-image
```

### Après (FLUX)
```bash
docker-compose up -d
# Port 8188 - ComfyUI
# API: http://localhost:3000/generate-image (même endpoint !)
```

## 🚀 Premier démarrage

```bash
# 1. Pull les changements
git pull

# 2. Reconstruire les images
docker-compose down
docker-compose build flux-comfyui

# 3. Démarrer (télécharge automatiquement FLUX ~33GB)
docker-compose up -d flux-comfyui

# 4. Attendre le téléchargement (10-30 min selon connexion)
docker logs -f claudine-flux

# 5. Tester
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "grandmother in JoJo bizarre adventure style",
    "width": 1024,
    "height": 1024,
    "steps": 4
  }'
```

## ⚙️ Configuration recommandée

### Pour FLUX.1-schnell (rapide)
```json
{
  "width": 1024,
  "height": 1024,
  "steps": 4,
  "model_name": "flux1-schnell"
}
```

### Pour FLUX.1-dev (qualité)
```json
{
  "width": 1024,
  "height": 1024,
  "steps": 25,
  "model_name": "flux1-dev"
}
```

## 💾 Espace disque requis

- **Modèles FLUX** : ~33 GB
  - flux1-schnell.safetensors : 12 GB
  - clip_l.safetensors : 1 GB
  - t5xxl_fp16.safetensors : 9 GB
  - ae.safetensors : 335 MB

## 🖥️ Ressources système

### CPU (lent, mais fonctionne)
- RAM : 32 GB minimum
- Temps : ~2-3 min par image

### GPU NVIDIA (recommandé)
- VRAM : 12 GB minimum (RTX 3060 12GB, RTX 4070+)
- Temps : ~3-5s par image (schnell), ~15-30s (dev)

## 🔧 Activer GPU (Windows/Linux)

Dans `docker-compose.yml`, décommenter :

```yaml
flux-comfyui:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

Puis :
```bash
docker-compose down
docker-compose up -d
```

## 📝 API - Pas de changement !

L'API reste **identique**, seul le moteur change :

```python
# Ça marche toujours pareil !
curl -X POST http://localhost:3000/generate-image \
  -d '{"prompt": "beautiful landscape"}'
```

## 🎨 Qualité des prompts

FLUX comprend **beaucoup mieux** les prompts :

**Avant (SD) :**
```
"pixel art knight character, blue armor, side view, game sprite, 8-bit style"
→ Résultat moyen, incohérent
```

**Après (FLUX) :**
```
"pixel art knight character, blue armor"
→ Excellent résultat, comprend naturellement
```

## 🐛 Troubleshooting

### Erreur "Out of memory"
→ Augmenter RAM Docker ou utiliser GPU

### Téléchargement lent
→ Les modèles font 33GB, c'est normal

### ComfyUI ne démarre pas
```bash
docker logs claudine-flux
# Vérifier les erreurs
```

## 📊 Comparaison qualité

Testez vous-même :

```bash
# Test SD v1.5
curl -X POST http://localhost:3000/generate-image \
  -d '{"prompt": "cyberpunk city at night", "model_name": "v1-5-pruned-emaonly"}'

# Test FLUX
curl -X POST http://localhost:3000/generate-image \
  -d '{"prompt": "cyberpunk city at night", "model_name": "flux1-schnell"}'
```

→ La différence est **spectaculaire** 🚀
