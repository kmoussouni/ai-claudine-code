# Configuration Open WebUI pour la génération d'images

## Problème
Le modèle répond qu'il ne peut pas générer d'images au lieu d'utiliser la fonction.

## Solution : Activer les Tools

### Étape 1 : Ajouter la fonction

1. **Admin Panel** (icône admin en haut à droite)
2. **Functions**
3. **+ Create New Function**
4. Coller le code de `webui-functions/generate_image.py`
5. **Save & Enable**

### Étape 2 : Configurer le modèle pour utiliser les tools

**Option A : Via le chat**
1. Dans le chat, cliquez sur le nom du modèle en haut
2. Cherchez **"Tools"** ou **"Functions"**
3. Cochez **"Generate Image with Stable Diffusion"**
4. Testez : `Génère une image de chevalier`

**Option B : Via Model Settings**
1. Admin Panel → Models
2. Trouvez `qwen2.5-coder:32b`
3. Edit → Functions → Activer `generate_image`

### Étape 3 : System Prompt (si ça ne marche toujours pas)

Ajoutez ce System Prompt au modèle :

```
You are an AI assistant with access to image generation tools.

When a user asks you to generate, create, or draw an image, you MUST use the generate_image function instead of explaining how to code it.

Examples:
- User: "Generate an image of a knight"
  → Call generate_image("knight in armor")

- User: "Create a pixel art character"
  → Call generate_image("pixel art character")

NEVER write Python/PIL code to create images. ALWAYS use the generate_image function.
```

## Alternative : API directe

Si Open WebUI est trop compliqué, utilisez le script CLI :

```bash
python3 generate-image-cli.py "grandmother in JoJo style" --quality
```

## Vérifier que tout fonctionne

```bash
# 1. Vérifier que l'API est accessible
curl http://localhost:3000/sd/health

# 2. Tester la génération directe
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test image", "width": 512, "height": 512}'

# 3. Si ça marche, le problème vient d'Open WebUI
```
