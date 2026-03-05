# Intégration Open WebUI - Génération d'Images

Guide complet pour utiliser les fonctions de génération d'images directement depuis l'interface Open WebUI.

## 🎯 Vue d'Ensemble

Trois fonctions personnalisées permettent de générer des images depuis le chat Open WebUI :

| Fonction | Description | Cas d'Usage |
|----------|-------------|-------------|
| `generate_image` | Génération d'images personnalisée | Illustrations, concepts, assets génériques |
| `generate_spritesheet` | Spritesheets pour jeux | Animations de personnages, objets animés |
| `generate_game_asset` | Assets de jeux spécifiques | Icons, items, backgrounds, characters, tilesets |

## 🚀 Installation et Configuration

### Étape 1 : Démarrer les Services

```bash
# Redémarrer les services pour monter les fonctions
docker-compose down
docker-compose up -d

# Vérifier que WebUI a accès aux fonctions
docker-compose exec webui ls -la /app/backend/data/functions/
```

**Devrait afficher** :
```
generate_image.py
generate_spritesheet.py
generate_game_asset.py
```

### Étape 2 : Activer les Fonctions dans Open WebUI

1. Ouvrir Open WebUI : `http://localhost:8080` (ou `http://192.168.1.12:8080`)
2. Se connecter (créer un compte si premier démarrage)
3. Cliquer sur votre profil → **Settings**
4. Aller dans l'onglet **Functions**
5. Les 3 fonctions devraient apparaître automatiquement
6. **Activer** chaque fonction (toggle switch)

### Étape 3 : Configuration des Valves (Optionnel)

Pour chaque fonction, vous pouvez configurer :

- **AGENT_API_URL** : URL de l'agent (défaut: `http://code-agent:3000`)
- **DEFAULT_STEPS** : Nombre d'étapes par défaut
- **DEFAULT_CFG_SCALE** : Échelle CFG par défaut

**Laisser les valeurs par défaut** fonctionne parfaitement dans Docker.

## 📝 Utilisation dans le Chat

### Méthode 1 : Demande Naturelle (Recommandée)

L'agent détecte automatiquement quand vous voulez générer une image :

```
User: Peux-tu générer une image d'un chevalier en pixel art avec une armure bleue ?

Agent: [Appelle automatiquement generate_image]
🎨 Image Generated Successfully!
📝 Prompt: pixel art character, knight with blue armor, game sprite
📏 Size: 512x512px
🎲 Seed: 123456789
💾 Saved to: /workspace/generated-images/20250106_abc123_seed123456789.png
```

### Méthode 2 : Appel Direct de Fonction

Vous pouvez aussi appeler les fonctions explicitement :

```python
# Génération d'image simple
generate_image("pixel art knight", width=512, height=512)

# Spritesheet
generate_spritesheet("knight walking", frames=8, frame_width=64)

# Game asset
generate_game_asset("item", "magic sword with flames", size=256)
```

## 🎨 Exemples d'Utilisation

### Exemple 1 : Icon de Potion

**Demande** :
```
Crée-moi une icône de potion de vie, style RPG, bouteille rouge avec liquide brillant
```

**Résultat** :
```
⚔️ Game Asset Generated Successfully!
📦 Type: Item
📝 Description: game item, health potion red liquid glass bottle, pixel art, RPG style...
📏 Size: 512x512px
💾 Saved to: .../generated-images/20250106_xyz789_seed987654.png

Tips for using in your game:
- Great for inventory systems and loot drops
- Can be used as-is or as reference for pixel art
- Consider adding glow/outline for rarity tiers
```

### Exemple 2 : Spritesheet de Marche

**Demande** :
```
Je veux un spritesheet d'un chevalier qui marche, 8 frames, vue de côté
```

**Résultat** :
```
🎮 Spritesheet Generated Successfully!
📝 Description: knight character walking animation, side view...
🎞️ Frames: 8 frames
📏 Frame Size: 64x64px
📐 Total Size: 512x64px
💾 Saved to: .../generated-images/...

Usage in Unity:
1. Import the spritesheet into your Unity project
2. Set Texture Type to "Sprite (2D and UI)"
3. Set Sprite Mode to "Multiple"
4. Open Sprite Editor and slice into 8 frames (64x64 each)
5. Create an animation using the frames
```

### Exemple 3 : Background de Niveau

**Demande** :
```
Génère un background pour un niveau dans une forêt mystique, style 2D platformer
```

**Résultat** :
```
🏞️ Game Asset Generated Successfully!
📦 Type: Background
📝 Description: game background, mystical forest, 2D platformer style...
📏 Size: 1024x512px

Tips for using in your game:
- Can be used as parallax layers
- May need seamless tiling adjustments
- Consider color grading for different times of day
```

## 🎮 Workflow de Création de Jeu Complet

### Scénario : Créer un Personnage Joueur

**Conversation complète** :

```
User: Je veux créer un personnage de chevalier pour mon jeu 2D

Agent: Super ! Je peux t'aider à créer plusieurs assets :
1. Un spritesheet d'animation
2. Des icons d'items
3. Un background pour le niveau

Commençons par le spritesheet ?

User: Oui, génère un spritesheet de marche, 8 frames, vue de côté

Agent: [Génère le spritesheet]
🎮 Spritesheet Generated Successfully!
...

User: Maintenant je veux une épée magique pour ce chevalier

Agent: [Génère l'item]
⚔️ Game Asset Generated Successfully!
Type: Item
Description: magic sword for knight character...

User: Et un château en background

Agent: [Génère le background]
🏞️ Game Asset Generated Successfully!
Type: Background
Description: medieval castle background...
```

### Résultat

En une seule conversation, vous avez :
- ✅ Spritesheet du personnage (animation de marche)
- ✅ Item (épée magique)
- ✅ Background (château)

Tous sauvegardés dans `/workspace/generated-images/` et prêts à être importés dans Unity/Godot !

## 🔧 Paramètres Avancés

### Contrôler la Qualité

```
User: Génère une image de haute qualité d'un dragon, avec 50 étapes de diffusion

Agent: [Appelle avec steps=50 pour meilleure qualité]
```

### Negative Prompts

```
User: Crée un personnage de chevalier, mais surtout pas en 3D ni réaliste

Agent: [Utilise negative_prompt="3d, realistic, photo"]
```

### Tailles Personnalisées

```
User: Je veux une bannière horizontale de 1024x256 pour mon jeu

Agent: [Génère avec width=1024, height=256]
```

### Seed Spécifique (Reproductibilité)

```
User: J'ai aimé l'image précédente (seed 123456), peux-tu en générer une similaire ?

Agent: [Utilise seed=123456 pour des résultats similaires]
```

## 📂 Accéder aux Images Générées

### Depuis le Serveur

```bash
# Lister toutes les images générées
ls -lh /workspace/generated-images/

# Copier une image vers le Mac
scp user@192.168.1.12:/path/to/generated-images/image.png ~/Downloads/
```

### Depuis Open WebUI (Futur)

Les images sont montées dans `/app/backend/static/generated-images` et seront potentiellement accessibles via :
```
http://localhost:8080/static/generated-images/[filename].png
```

### Organisation Recommandée

Créer des sous-dossiers par projet :

```bash
workspace/generated-images/
├── project-rpg/
│   ├── characters/
│   ├── items/
│   └── backgrounds/
├── project-platformer/
│   └── sprites/
└── tests/
```

## 🎯 Best Practices

### Prompts Efficaces

**❌ Mauvais** :
```
"un truc pour mon jeu"
```

**✅ Bon** :
```
"pixel art character sprite, knight with blue armor, side view, game asset, 16-bit style"
```

### Itération Rapide

1. **Commencer simple** : Générer un asset de base
2. **Raffiner** : Ajuster le prompt avec plus de détails
3. **Optimiser** : Jouer avec steps, CFG scale
4. **Standardiser** : Utiliser les mêmes seeds pour cohérence

### Cohérence Visuelle

Pour un jeu cohérent :
- **Même style** : "pixel art 16-bit" dans tous les prompts
- **Même palette** : Mentionner les couleurs principales
- **Même perspective** : Toujours "side view" ou "top-down"

## ⚡ Performance

### Temps de Génération

| Configuration | Temps Moyen |
|---------------|-------------|
| GPU RTX 3060+ | 5-10 secondes |
| GPU RTX 4070+ | 3-5 secondes |
| CPU seul | 2-5 minutes |

### Optimisations

- **Réduire les steps** : 15-20 pour tests rapides
- **Taille modérée** : 512x512 est un bon équilibre
- **Batch generation** : Générer plusieurs assets en une session

## 🐛 Dépannage

### "Error: 503 - SD n'est pas activé"

```bash
# Vérifier que SD tourne
docker-compose ps stable-diffusion

# Redémarrer si nécessaire
docker-compose restart stable-diffusion
```

### "Timeout après 5 minutes"

- Réduire le nombre de steps
- Réduire la taille de l'image
- Vérifier que le GPU est utilisé

### Fonctions pas visibles dans Open WebUI

```bash
# Vérifier le montage des volumes
docker-compose down
docker-compose up -d

# Vérifier les logs WebUI
docker-compose logs webui | grep -i function
```

## 📚 Ressources

- [STABLE-DIFFUSION.md](STABLE-DIFFUSION.md) - Guide technique SD
- [TESTING-PHASE1.md](TESTING-PHASE1.md) - Tests backend
- [PHASE1-IMAGE-GENERATION.md](PHASE1-IMAGE-GENERATION.md) - Architecture

---

**Prêt à créer des assets de jeu ? Ouvrez Open WebUI et commencez à discuter avec l'agent ! 🎮**
