# Open WebUI Functions - Claudine

Fonctions personnalisées pour Open WebUI permettant la génération d'images via Stable Diffusion.

## 📚 Fonctions Disponibles

| Fonction | Description | Usage |
|----------|-------------|-------|
| `generate_image.py` | Génération d'images personnalisée | `/generate_image "pixel art knight"` |
| `generate_spritesheet.py` | Spritesheets pour jeux vidéo | `/generate_spritesheet "walking knight" frames=8` |
| `generate_game_asset.py` | Assets de jeux (icons, items) | `/generate_game_asset type=item "magic sword"` |

## 🔧 Installation

### Méthode 1 : Via l'Interface Open WebUI

1. Ouvrir Open WebUI : `http://localhost:8080`
2. Aller dans **Settings** → **Functions**
3. Cliquer **+ Add Function**
4. Copier-coller le contenu de chaque fichier `.py`
5. Sauvegarder et activer

### Méthode 2 : Via Volume Docker

```bash
# Copier les fonctions dans le volume Open WebUI
docker cp webui-functions/. claudine-webui:/app/backend/data/functions/

# Redémarrer Open WebUI
docker-compose restart webui
```

### Méthode 3 : Via docker-compose (Recommandé)

Ajouter un volume mount dans `docker-compose.yml` :

```yaml
webui:
  volumes:
    - webui_data:/app/backend/data
    - ./webui-functions:/app/backend/data/functions  # ← Ajouter cette ligne
```

Puis redémarrer :
```bash
docker-compose restart webui
```

## 📝 Utilisation dans le Chat

### Générer une Image Simple

```
User: Peux-tu générer une image d'un chevalier en pixel art ?

Agent: [Appelle automatiquement generate_image]
🎨 Image Generated Successfully!
...
```

### Générer un Spritesheet

```
User: Crée un spritesheet de marche pour un personnage, 8 frames

Agent: [Appelle generate_spritesheet]
🎮 Spritesheet Generated Successfully!
...
```

### Générer un Asset de Jeu

```
User: Je veux une icône de potion de vie style RPG

Agent: [Appelle generate_game_asset]
⚔️ Game Asset Generated Successfully!
...
```

## 🔧 Paramètres des Fonctions

### generate_image

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| prompt | string | requis | Description de l'image |
| width | int | 512 | Largeur en pixels |
| height | int | 512 | Hauteur en pixels |
| steps | int | 20 | Nombre d'étapes de diffusion |
| negative_prompt | string | null | Ce qu'on ne veut PAS |

### generate_spritesheet

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| prompt | string | requis | Description du sprite |
| frames | int | 4 | Nombre de frames |
| frame_width | int | 64 | Largeur par frame |
| frame_height | int | 64 | Hauteur par frame |
| steps | int | 30 | Étapes de diffusion |

### generate_game_asset

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| asset_type | string | requis | icon, item, background, character, tileset |
| description | string | requis | Description de l'asset |
| size | int | 512 | Taille (carré) |
| steps | int | 25 | Étapes de diffusion |

## 📚 Documentation Complète

Voir [WEBUI-INTEGRATION.md](../WEBUI-INTEGRATION.md) pour le guide complet d'utilisation avec exemples détaillés