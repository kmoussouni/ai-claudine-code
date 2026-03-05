# Démarrage Rapide des Tests - Phase 1

Guide express pour lancer les tests de validation Phase 1.

## 🚀 Préparation (5 minutes)

### Sur le Serveur (192.168.1.12)

```bash
# 1. Aller dans le dossier projet
cd ~/ai/ai-claudine-code

# 2. Récupérer les derniers changements
git fetch origin
git checkout feature/image-generation
git pull origin feature/image-generation

# 3. Vérifier qu'on a les bons fichiers
ls -la scripts/run-tests.sh
ls -la CAHIER-RECETTE-PHASE1.md

# 4. Rendre le script exécutable (si nécessaire)
chmod +x scripts/run-tests.sh
```

## 🏗️ Étape 1 : Déploiement (2-3 minutes)

```bash
# Arrêter services existants
docker-compose down

# Rebuilder l'agent (nouveaux services Python)
docker-compose build code-agent

# Démarrer TOUS les services
docker-compose up -d

# Attendre 30 secondes que tout démarre
sleep 30

# Vérifier statut
docker-compose ps
```

**✅ Résultat attendu** : 4 services `Running`
- `claudine-ollama`
- `claudine-agent`
- `claudine-webui`
- `claudine-sd`

## 🎨 Étape 2 : Setup Stable Diffusion (5-10 minutes)

```bash
# Vérifier que SD est accessible
make sd-setup

# Télécharger le modèle SD 1.5 (4 GB - prend 5-10 min)
make sd-download
# → Choisir option 1
# → Confirmer avec 'o' ou 'y'

# Attendre fin du téléchargement
# Puis redémarrer SD
docker-compose restart stable-diffusion

# Attendre 30 secondes
sleep 30

# Vérifier que le modèle est chargé
make sd-models
```

**✅ Résultat attendu** :
```
📦 Modèles Stable Diffusion installés :
   - v1-5-pruned-emaonly.safetensors
```

## 🧪 Étape 3 : Tests Automatisés (1 minute)

```bash
# Lancer le script de tests automatisés
./scripts/run-tests.sh
```

Ce script va tester :
- ✅ Infrastructure Docker
- ✅ Volumes montés
- ✅ Connectivité services
- ✅ Stable Diffusion API
- ✅ Agent API endpoints
- ✅ Fichiers sauvegardés

**✅ Résultat attendu** :
```
╔═══════════════════════════════════════════════════════════╗
║   ✅ TOUS LES TESTS AUTOMATISÉS RÉUSSIS !                ║
╚═══════════════════════════════════════════════════════════╝
```

**Résultats sauvegardés** dans `test-results-phase1.txt`

## 🖼️ Étape 4 : Test Génération Rapide (30 secondes)

```bash
# Test génération d'une image simple
curl -X POST http://localhost:3000/generate-image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pixel art knight, blue armor, game sprite",
    "width": 512,
    "height": 512,
    "steps": 20
  }' | python3 -m json.tool
```

**✅ Résultat attendu** :
```json
{
  "status": "success",
  "image_path": "/workspace/generated-images/20250106_XXXXXX_seedXXXX.png",
  "seed": 123456789,
  ...
}
```

**Vérifier l'image** :
```bash
ls -lh workspace/generated-images/
# Devrait montrer un fichier PNG récent
```

## 🌐 Étape 5 : Test Interface WebUI (5 minutes)

### 5a. Accès Interface

```bash
# Ouvrir dans navigateur
make sd-ui
# Ou manuellement : http://localhost:7860
```

**Test manuel** :
1. Interface SD s'ouvre
2. Prompt : `pixel art character, knight`
3. Cliquer **Generate**
4. Image générée en 5-30 secondes

### 5b. Open WebUI

Depuis votre **Mac**, ouvrir : `http://192.168.1.12:8080`

1. **Créer compte** (si première fois)
2. **Settings** → **Functions**
3. **Vérifier** que 3 fonctions sont présentes :
   - Generate Image with Stable Diffusion
   - Generate Spritesheet
   - Generate Game Asset
4. **Activer** les 3 fonctions (toggle ON)

### 5c. Test Chat

Dans Open WebUI, nouvelle conversation :

```
User: Peux-tu générer une image d'un chevalier en pixel art avec une armure bleue ?
```

**✅ Résultat attendu** :
```
🎨 Image Generated Successfully!

📝 Prompt: pixel art character, knight with blue armor...
📏 Size: 512x512px
🎲 Seed: 123456789
💾 Saved to: /workspace/generated-images/...
```

## ✅ Checklist Rapide

Validation minimale avant merge :

- [ ] **Infrastructure** : 4 services running
- [ ] **SD Setup** : Modèle SD 1.5 installé
- [ ] **Tests Auto** : Script tests OK (0 failed)
- [ ] **API** : Une image générée via curl
- [ ] **SD UI** : Interface accessible et génération OK
- [ ] **Open WebUI** : Fonctions visibles et activées
- [ ] **Chat** : Génération d'image via chat fonctionne

**Si tous ✅** : Prêt pour merge dans dev !

## 🐛 Dépannage Express

### "Service SD not running"
```bash
docker-compose restart stable-diffusion
sleep 30
```

### "No module named httpx"
```bash
docker-compose build code-agent
docker-compose restart code-agent
```

### "Connection refused" depuis Mac
```bash
# Vérifier que services écoutent sur 0.0.0.0
docker-compose logs code-agent | grep "0.0.0.0"
```

### Fonctions WebUI pas visibles
```bash
docker-compose exec webui ls /app/backend/data/functions/
# Devrait montrer generate_*.py

# Si vide :
docker-compose down
docker-compose up -d
```

## 📚 Aller Plus Loin

### Tests Complets
```bash
# Cahier de recette complet (25 tests)
cat CAHIER-RECETTE-PHASE1.md
```

### Performance
```bash
# Vérifier utilisation GPU
docker-compose logs stable-diffusion | grep -i cuda
docker-compose logs stable-diffusion | grep -i gpu
```

### Logs
```bash
# Tous les logs
docker-compose logs -f

# Logs spécifiques
docker-compose logs -f stable-diffusion
docker-compose logs -f code-agent
```

## 🎯 Temps Total Estimé

| Étape | Temps |
|-------|-------|
| Préparation | 5 min |
| Déploiement | 3 min |
| Setup SD + Modèle | 10 min |
| Tests Auto | 1 min |
| Test Génération | 1 min |
| Test WebUI | 5 min |
| **TOTAL** | **~25 minutes** |

---

**Prêt ? Commencez par l'Étape 1 sur le serveur !** 🚀
