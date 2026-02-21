# Démarrage Rapide - Claudine

Guide ultra-rapide pour démarrer avec Claudine en 5 minutes.

## Installation Express

```bash
# 1. Configuration initiale (télécharge le modèle)
./scripts/setup.sh

# 2. Démarrer tous les services
./scripts/start.sh

# 3. Vérifier que tout fonctionne
python3 scripts/cli.py health
```

C'est tout ! 🎉

## Accéder aux Interfaces

- **Interface Web** : http://localhost:8080
- **API Documentation** : http://localhost:3000/docs
- **Ollama API** : http://localhost:11434

## Premier Test

### Via Interface Web

1. Ouvrir http://localhost:8080
2. Créer un compte (reste en local)
3. Taper : "Crée une fonction Python qui calcule fibonacci"

### Via CLI

```bash
python3 scripts/cli.py chat "Crée un fichier hello.py qui affiche Hello World"
```

Le fichier sera créé dans `workspace/hello.py`

### Via API

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Crée une fonction pour valider un email"}'
```

## Exemples Pratiques

### Créer un nouveau fichier

```bash
python3 scripts/cli.py chat "Crée workspace/api.py avec un serveur FastAPI basique"
```

### Modifier un fichier existant

```bash
python3 scripts/cli.py chat "Ajoute la gestion d'erreurs" --files workspace/api.py
```

### Générer des tests

```bash
python3 scripts/cli.py chat "Crée des tests pytest" --files workspace/api.py
```

## Intégration VS Code

### Installation

1. Installer l'extension "Continue" dans VS Code
2. Copier la configuration :

```bash
# Créer le dossier si nécessaire
mkdir -p ~/.continue

# Copier la config
cp config.continue.json ~/.continue/config.json
```

3. Recharger VS Code (`Cmd/Ctrl + Shift + P` → "Reload Window")

### Utilisation

- `Cmd/Ctrl + L` : Ouvrir le chat
- `Cmd/Ctrl + I` : Modifier le code
- Taper `/` pour voir les commandes custom

## Commandes Utiles

```bash
# Démarrer
make start

# Arrêter
make stop

# Voir les logs
make logs

# État des services
make status

# Lister les modèles
make models

# Télécharger un modèle
make pull MODEL=qwen2.5-coder:32b
```

## Changer de Modèle

Par défaut, Claudine utilise `qwen2.5-coder:7b`.

### Télécharger un autre modèle

```bash
# Modèle plus puissant (nécessite 32 GB RAM)
./scripts/pull-model.sh qwen2.5-coder:32b

# Autre option excellente
./scripts/pull-model.sh deepseek-coder-v2:16b
```

### Utiliser le nouveau modèle

**Via CLI :**
```bash
python3 scripts/cli.py chat "votre message" --model qwen2.5-coder:32b
```

**Par défaut :**
Éditez `.env` et changez :
```bash
DEFAULT_MODEL=qwen2.5-coder:32b
```

Puis redémarrez :
```bash
make restart
```

## Configuration Minimale vs Puissante

### Configuration Légère (Mac Air M4 / 16GB RAM)

```bash
# Modèle par défaut (déjà installé)
# qwen2.5-coder:7b
# Rapide et efficace
```

### Configuration Puissante (32-64GB RAM)

```bash
# Télécharger le modèle plus puissant
./scripts/pull-model.sh qwen2.5-coder:32b

# Changer dans .env
echo "DEFAULT_MODEL=qwen2.5-coder:32b" >> .env

# Redémarrer
make restart
```

## Workflow Recommandé

### Pour Développement Quotidien

1. **Démarrer le matin**
   ```bash
   make start
   ```

2. **Travailler avec VS Code + Continue**
   - Extension Continue connectée à Claudine
   - Autocomplétion instantanée
   - Chat dans l'éditeur

3. **Tâches lourdes via CLI**
   ```bash
   python3 scripts/cli.py chat "Refactor complet de ce module" \
     --files workspace/complex_module.py
   ```

4. **Arrêter le soir**
   ```bash
   make stop
   ```

### Pour Projets Importants

1. **Copier le projet dans workspace**
   ```bash
   cp -r ~/mon-projet workspace/
   ```

2. **Demander une analyse**
   ```bash
   python3 scripts/cli.py chat "Analyse l'architecture et propose des améliorations" \
     --files workspace/mon-projet/src/*.py
   ```

3. **Modifications itératives**
   ```bash
   # Première passe
   python3 scripts/cli.py chat "Ajoute validation des données" \
     --files workspace/mon-projet/models.py

   # Deuxième passe
   python3 scripts/cli.py chat "Ajoute les tests pour la validation" \
     --files workspace/mon-projet/models.py
   ```

## Résolution Rapide des Problèmes

### Les services ne démarrent pas

```bash
# Vérifier Docker
docker ps

# Redémarrer complètement
make stop
make start
```

### L'agent ne répond pas

```bash
# Vérifier la santé
python3 scripts/cli.py health

# Voir les logs
make logs
```

### "Out of memory"

Utilisez un modèle plus petit :
```bash
./scripts/pull-model.sh codellama:7b
echo "DEFAULT_MODEL=codellama:7b" >> .env
make restart
```

### Performance lente

- Utilisez modèle 7B au lieu de 32B
- Sur Mac M-series, vérifiez Docker → Settings → Use Rosetta

## Prochaines Étapes

Maintenant que Claudine fonctionne :

1. **Explorez les exemples** : `less EXAMPLES.md`
2. **Configurez votre IDE** : `less INTEGRATION.md`
3. **Lisez la doc complète** : `less README.md`

## Support

- **Documentation** : README.md, INTEGRATION.md, EXAMPLES.md
- **Problèmes** : Ouvrir une issue GitHub
- **Logs** : `make logs` ou `docker-compose logs -f`

## Ressources

- [Ollama Models](https://ollama.com/library)
- [Continue Extension](https://continue.dev)
- [Aider Documentation](https://aider.chat)

---

**Bon coding ! 🚀**

Pour aller plus loin, consultez README.md pour la documentation complète.
