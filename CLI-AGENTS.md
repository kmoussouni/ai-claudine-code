# Agents CLI Claudine

Claudine propose **3 agents CLI différents** pour s'adapter à votre workflow préféré. Choisissez celui qui vous convient le mieux !

## Vue d'Ensemble

| Agent | Type | Niveau | Meilleur Pour |
|-------|------|--------|---------------|
| **Agent Interactif** | Python | Débutant | Usage quotidien, sessions conversationnelles |
| **Agent Aider** | Natif | Intermédiaire | Modifications de code directes, power users |
| **Agent TUI** | Interface riche | Avancé | Multi-tâches, vue d'ensemble, interface moderne |

---

## 1. Agent Interactif (Recommandé pour débuter)

### Description

Agent conversationnel en Python, simple et intuitif. Session de chat interactive avec historique et gestion de contexte.

### Lancement

```bash
python3 scripts/agent-interactive.py
```

### Fonctionnalités

- ✅ Session conversationnelle continue
- ✅ Historique des commandes (flèches haut/bas)
- ✅ Gestion du contexte de fichiers
- ✅ Changement de modèle à la volée
- ✅ Coloration syntaxique
- ✅ Sauvegarde automatique de l'historique

### Commandes Spéciales

```
:help              Afficher l'aide
:model <nom>       Changer de modèle
:files [f1 f2 ..]  Définir les fichiers de contexte
:clear             Effacer le contexte et l'historique
:history           Voir l'historique de la conversation
:workspace         Lister les fichiers du workspace
:exit / :quit      Quitter
```

### Exemple de Session

```
You> Crée un fichier hello.py qui affiche Hello World

🤖 Agent réfléchit...

Agent>
J'ai créé le fichier workspace/hello.py avec le code suivant:

```python
print("Hello World")
```

You> :files workspace/hello.py

✓ Fichiers de contexte: workspace/hello.py

You [1 fichiers]> Ajoute une fonction main() et un if __name__ == '__main__'

🤖 Agent réfléchit...

Agent>
J'ai modifié le fichier avec une structure plus propre:
[...]
```

### Avantages

- 🟢 Simple à utiliser
- 🟢 Parfait pour débuter
- 🟢 Historique persistant
- 🟢 Gestion de contexte facile

### Inconvénients

- 🔴 Interface basique
- 🔴 Pas de prévisualisation de code

---

## 2. Agent Aider (Pour les Power Users)

### Description

Wrapper pour utiliser **Aider** directement. Aider est un outil CLI puissant spécialisé dans les modifications de code.

### Prérequis

Assurez-vous que les services Docker sont démarrés :
```bash
make start
```

### Lancement

```bash
./scripts/agent-aider.sh

# Ou avec des fichiers spécifiques
./scripts/agent-aider.sh workspace/file1.py workspace/file2.py
```

### Commandes Aider

```
/help           Aide complète
/add <file>     Ajouter un fichier au contexte
/drop <file>    Retirer un fichier du contexte
/ls             Lister les fichiers en contexte
/clear          Effacer l'historique
/undo           Annuler la dernière modification
/diff           Voir les changements
/commit         Créer un commit git
/exit           Quitter
```

### Exemple de Session

```bash
$ ./scripts/agent-aider.sh

Aider v0.x.x
Model: qwen2.5-coder:7b
Working directory: /workspace

> /add server.py

Added server.py to the chat

> Ajoute la validation des entrées avec Pydantic

[Aider modifie directement le fichier]

> /diff

[Affiche les changements effectués]

> /commit "feat: add input validation"

[Crée un commit git]
```

### Avantages

- 🟢 Très puissant pour modifications de code
- 🟢 Intégration Git native
- 🟢 Commandes spécialisées code
- 🟢 Support multi-fichiers avancé
- 🟢 Peut annuler les modifications (/undo)

### Inconvénients

- 🔴 Courbe d'apprentissage plus élevée
- 🔴 Nécessite de connaître les commandes Aider
- 🔴 Moins conversationnel

### Cas d'Usage Idéaux

- Refactoring de code existant
- Modifications précises sur plusieurs fichiers
- Workflow avec Git
- Développeurs expérimentés

---

## 3. Agent TUI (Interface Moderne)

### Description

Interface terminal moderne avec **interface splitée** : chat à gauche, informations à droite. Utilise Textual pour une UI riche.

### Installation des Dépendances

```bash
pip3 install textual
```

### Lancement

```bash
python3 scripts/agent-tui.py
```

### Interface

```
┌─────────────────────────────────────────────────────────────┐
│                    Claudine Header                          │
├──────────────────────────────────┬──────────────────────────┤
│                                  │  📁 Fichiers en contexte │
│         Zone de Chat             │  • file1.py              │
│                                  │  • file2.py              │
│  You: Message...                 │                          │
│  Agent: Réponse...               │  💡 Raccourcis           │
│                                  │  Ctrl+C Quitter          │
│                                  │  Ctrl+L Effacer          │
│                                  │                          │
│                                  │  📝 Commandes            │
│                                  │  :files  Gérer fichiers  │
│                                  │  :model  Changer modèle  │
├──────────────────────────────────┴──────────────────────────┤
│  [Input: Votre message...]              [Bouton: Envoyer]   │
├──────────────────────────────────────────────────────────────┤
│  Status: Connecté | Modèle: qwen2.5-coder:7b               │
└──────────────────────────────────────────────────────────────┘
```

### Fonctionnalités

- ✅ Interface graphique dans le terminal
- ✅ Vue splitée (chat + sidebar)
- ✅ Barre de statut en temps réel
- ✅ Boutons cliquables
- ✅ Raccourcis clavier
- ✅ Coloration et formatting riches
- ✅ Scrolling fluide

### Raccourcis Clavier

```
Ctrl+C          Quitter
Ctrl+L          Effacer l'historique
Entrée          Envoyer le message
Tab             Naviguer entre les widgets
```

### Commandes

```
:help              Afficher l'aide
:files [...]       Définir les fichiers de contexte
:model <nom>       Changer de modèle
:clear             Effacer l'historique
```

### Avantages

- 🟢 Interface moderne et élégante
- 🟢 Vue d'ensemble complète
- 🟢 Meilleure organisation visuelle
- 🟢 Boutons cliquables
- 🟢 Multi-tâches plus facile

### Inconvénients

- 🔴 Dépendance supplémentaire (textual)
- 🔴 Plus lourd que les autres options
- 🔴 Peut avoir des problèmes sur certains terminaux

### Cas d'Usage Idéaux

- Sessions longues avec beaucoup de contexte
- Besoin de vue d'ensemble
- Amateurs d'interfaces modernes
- Multi-tâches

---

## Comparaison Détaillée

### Performance

| Agent | Démarrage | Mémoire | CPU |
|-------|-----------|---------|-----|
| Interactif | ⚡ Rapide | 🟢 Faible | 🟢 Faible |
| Aider | ⚡ Rapide | 🟢 Faible | 🟢 Faible |
| TUI | 🟡 Moyen | 🟡 Moyen | 🟡 Moyen |

### Facilité d'Usage

| Agent | Courbe | Pour Débutants | Documentation |
|-------|--------|----------------|---------------|
| Interactif | 🟢 Facile | ✅ Oui | Intégrée |
| Aider | 🟡 Moyenne | 🟡 Moyen | Externe |
| TUI | 🟢 Facile | ✅ Oui | Intégrée |

### Fonctionnalités

| Fonctionnalité | Interactif | Aider | TUI |
|----------------|------------|-------|-----|
| Chat | ✅ | ✅ | ✅ |
| Contexte fichiers | ✅ | ✅ | ✅ |
| Historique | ✅ | ✅ | ✅ |
| Git intégré | ❌ | ✅ | ❌ |
| Interface riche | 🟡 | ❌ | ✅ |
| Undo | ❌ | ✅ | ❌ |
| Multi-fenêtres | ❌ | ❌ | ✅ |

---

## Quel Agent Choisir ?

### 🎯 Vous débutez avec Claudine ?
→ **Agent Interactif** (`agent-interactive.py`)

### 🎯 Vous êtes développeur expérimenté et voulez modifier du code précisément ?
→ **Agent Aider** (`agent-aider.sh`)

### 🎯 Vous aimez les belles interfaces et les sessions longues ?
→ **Agent TUI** (`agent-tui.py`)

### 🎯 Vous voulez essayer les 3 ?
Chacun a ses forces, alternez selon vos besoins !

---

## Installation des Dépendances

### Agent Interactif
```bash
pip3 install httpx
```

### Agent Aider
```bash
# Déjà installé dans le container Docker
# Aucune dépendance locale nécessaire
```

### Agent TUI
```bash
pip3 install textual httpx
```

---

## Workflow Recommandé

### Développement Quotidien
1. Démarrer les services : `make start`
2. Lancer l'**Agent Interactif** pour le chat général
3. Utiliser l'**Agent Aider** pour les modifications complexes
4. Lancer l'**Agent TUI** pour les sessions longues

### Quick Tasks
```bash
# Pour une question rapide
python3 scripts/cli.py chat "question rapide"

# Pour une session interactive
python3 scripts/agent-interactive.py
```

### Refactoring Important
```bash
# Utiliser Aider avec Git
./scripts/agent-aider.sh workspace/module.py

> Refactor cette classe pour utiliser le pattern Strategy
> /diff
> /commit "refactor: apply strategy pattern"
```

### Sessions Longues avec Contexte
```bash
# TUI pour vue d'ensemble
python3 scripts/agent-tui.py

# Ajouter plusieurs fichiers en contexte
:files workspace/models.py workspace/api.py workspace/tests.py

# Travailler avec vision complète
```

---

## Dépannage

### "Module not found"
```bash
pip3 install httpx textual
```

### "Connection refused"
```bash
# Démarrer les services
make start

# Vérifier qu'ils tournent
make status
```

### Agent TUI affichage bizarre
```bash
# Certains terminaux ont des problèmes
# Essayez avec iTerm2 sur Mac ou Windows Terminal

# Ou utilisez l'Agent Interactif à la place
python3 scripts/agent-interactive.py
```

### Aider ne démarre pas
```bash
# Vérifier que le container tourne
docker-compose ps

# Redémarrer si nécessaire
make restart
```

---

## Tips & Astuces

### Agent Interactif
- Utilisez les flèches ↑↓ pour naviguer dans l'historique
- `:files` sans arguments efface le contexte
- L'historique est sauvegardé dans `~/.claudine_history`

### Agent Aider
- `/add *.py` ajoute tous les fichiers Python
- `/diff` avant `/commit` pour vérifier les changements
- `/undo` pour annuler la dernière modification

### Agent TUI
- `Tab` pour naviguer entre input et bouton
- `Ctrl+L` efface rapidement l'écran
- La sidebar montre toujours le contexte actuel

---

## Ressources

- **Documentation Aider** : https://aider.chat/docs/
- **Documentation Textual** : https://textual.textualize.io/
- **Guide Claudine** : README.md
- **Exemples** : EXAMPLES.md

---

**Amusez-vous bien avec les 3 agents ! 🚀**

Chaque agent a été conçu pour un usage spécifique. N'hésitez pas à tous les essayer pour trouver votre préféré.
