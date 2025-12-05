# Test Rapide des 3 Agents CLI

Guide pour tester rapidement les 3 agents CLI de Claudine.

## Préparation

### 1. Démarrer les services Docker
```bash
make start
```

### 2. Installer les dépendances CLI
```bash
./scripts/install-cli-deps.sh
```

Cela installe :
- `httpx` (requis pour tous)
- `textual` (requis pour l'Agent TUI)
- `rich` et `pygments` (optionnels)

## Test 1 : Agent Interactif

### Lancement
```bash
python3 scripts/agent-interactive.py
```

### Test à faire
```
You> Crée un fichier workspace/hello.py qui affiche "Bonjour Claudine"

[Attendez la réponse]

You> :files workspace/hello.py

You [1 fichiers]> Ajoute une fonction main() et docstrings

[Attendez la réponse]

You> :history

You> :exit
```

### Ce que vous devriez voir
- ✅ Bannière de bienvenue colorée
- ✅ Réponse de l'agent avec le code généré
- ✅ Fichier créé dans `workspace/hello.py`
- ✅ Contexte mis à jour avec le fichier
- ✅ Historique de la conversation

---

## Test 2 : Agent Aider

### Lancement
```bash
./scripts/agent-aider.sh
```

### Test à faire
```
> /add workspace/hello.py

> Ajoute un argument en ligne de commande pour personnaliser le message

[Aider modifie le fichier]

> /diff

[Voir les changements]

> /exit
```

### Ce que vous devriez voir
- ✅ Bannière Aider
- ✅ Modèles disponibles listés
- ✅ Fichier ajouté au contexte
- ✅ Modifications appliquées directement
- ✅ Diff des changements

---

## Test 3 : Agent TUI

### Lancement
```bash
python3 scripts/agent-tui.py
```

### Test à faire
1. Tapez dans l'input en bas : `Explique le code de workspace/hello.py`
2. Appuyez sur Entrée ou cliquez sur "Envoyer"
3. Attendez la réponse dans la zone de chat
4. Tapez : `:files workspace/hello.py`
5. Observez la sidebar à droite qui s'update
6. Tapez : `Ajoute des tests unitaires`
7. Appuyez sur `Ctrl+C` pour quitter

### Ce que vous devriez voir
- ✅ Interface splitée (chat à gauche, sidebar à droite)
- ✅ Messages colorés et formatés
- ✅ Barre de statut en bas
- ✅ Sidebar montrant les fichiers en contexte
- ✅ Bouton "Envoyer" cliquable

---

## Comparaison Rapide

Après avoir testé les 3 :

### Agent Interactif
- ✅ Simple et rapide
- ✅ Bon pour questions/réponses
- ✅ Historique persistant
- 🤔 Interface basique

### Agent Aider
- ✅ Très puissant pour modifications de code
- ✅ Commandes spécialisées
- ✅ Intégration Git
- 🤔 Courbe d'apprentissage

### Agent TUI
- ✅ Interface moderne et élégante
- ✅ Vue d'ensemble claire
- ✅ Multi-tâches facile
- 🤔 Dépendance supplémentaire

## Scénario de Test Complet

Créez un petit projet pour tester tous les agents :

### Étape 1 : Avec Agent Interactif
```bash
python3 scripts/agent-interactive.py
```

```
You> Crée un projet simple dans workspace/calculator/ avec :
- calculator.py : classe Calculator avec add, subtract, multiply, divide
- main.py : script principal
- README.md : documentation
```

### Étape 2 : Avec Agent Aider
```bash
./scripts/agent-aider.sh workspace/calculator/calculator.py
```

```
> Ajoute la gestion des erreurs (division par zéro, etc.)
> /diff
> /commit "feat: add error handling"
```

### Étape 3 : Avec Agent TUI
```bash
python3 scripts/agent-tui.py
```

```
:files workspace/calculator/calculator.py
Crée des tests unitaires complets avec pytest
```

### Étape 4 : Vérification
```bash
# Voir ce qui a été créé
ls -la workspace/calculator/

# Lire un fichier
cat workspace/calculator/calculator.py

# Si git est initialisé par Aider
cd workspace/calculator
git log
```

## Dépannage

### "Module not found: httpx"
```bash
pip3 install httpx
```

### "Module not found: textual"
```bash
pip3 install textual
```

### "Connection refused"
```bash
# Démarrer les services
make start

# Vérifier
make status
```

### Agent TUI affichage bizarre
Utilisez un terminal moderne :
- macOS : iTerm2 ou Terminal.app natif
- Linux : GNOME Terminal, Konsole
- Windows : Windows Terminal

### Agent Aider ne démarre pas
```bash
# Vérifier que le container tourne
docker-compose ps

# Voir les logs
docker-compose logs code-agent

# Redémarrer si nécessaire
make restart
```

## Aller Plus Loin

### 1. Créer un vrai projet
```bash
python3 scripts/agent-interactive.py
```
```
You> Crée une API REST complète pour gérer des tâches (TODO app) avec FastAPI, SQLAlchemy, et tests pytest
```

### 2. Refactoring avec Aider
```bash
./scripts/agent-aider.sh workspace/todo-api/*.py
```
```
> Refactor pour utiliser le pattern Repository
> /commit "refactor: implement repository pattern"
```

### 3. Review avec TUI
```bash
python3 scripts/agent-tui.py
```
```
:files workspace/todo-api/models.py workspace/todo-api/api.py
Analyse le code et propose des améliorations de sécurité
```

## Feedback

Après avoir testé les 3 agents, notez vos préférences :

**Mon agent préféré :** _____________

**Pourquoi :** _____________________

**Cas d'usage idéal :** ______________

**Suggestions d'amélioration :** _______

---

Pour la documentation complète, voir [CLI-AGENTS.md](CLI-AGENTS.md)
