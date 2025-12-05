# Agent Smart - Agent Hybride Intelligent

L'**Agent Smart** est l'agent recommandé de Claudine. Il combine le meilleur des deux mondes : **conversation naturelle** ET **modification de code** avec système de permissions.

## 🌟 Caractéristiques Principales

- 💬 **Conversation Naturelle** : Répond à vos questions comme ChatGPT
- 📝 **Modification de Code** : Crée et modifie des fichiers quand nécessaire
- 🔍 **Compréhension du Projet** : Scanne et comprend votre structure de projet
- ✋ **Système de Permissions** : Demande toujours avant de modifier du code
- 🧠 **Détection d'Intention** : Sait automatiquement quoi faire selon votre demande

## 🚀 Lancement

```bash
# Via le launcher
./claudine-agent
# Puis choisir option 1

# Ou directement
python3 scripts/claudine-smart.py
```

## 💡 Exemples d'Utilisation

### 1. Conversation Normale

```
You> Quelles langues parles-tu ?

Claudine> Je parle principalement le français et l'anglais. Je peux comprendre
et générer du code dans de nombreux langages de programmation comme Python,
JavaScript, TypeScript, Java, etc.
```

**Résultat** : Réponse directe, pas de fichier créé ✅

### 2. Modification de Code (avec permission)

```
You> Crée un fichier calculator.py avec les opérations de base

⚠️  Permission requise:
Modifier le code: Crée un fichier calculator.py avec les opérations de base

Approuver? [o/N/toujours] : o

🔧 Exécution de la modification...

Claudine> [Aider crée le fichier calculator.py]
```

**Résultat** : Fichier créé après votre approbation ✅

### 3. Questions sur le Projet

```
You> Explique-moi la structure de mon projet

Claudine> Votre projet contient 12 fichiers principalement en Python (.py) et
JavaScript (.js). La structure montre que vous avez :
- Un répertoire src/ avec le code source
- Un dossier tests/ pour les tests
- Des fichiers de configuration à la racine
```

**Résultat** : Analyse du projet, pas de modification ✅

### 4. Auto-Approve pour Sessions Rapides

```
You> :auto on

You> Ajoute des docstrings à calculator.py

🔧 Exécution de la modification...
(Auto-approuvé)

Claudine> [Modifications appliquées automatiquement]
```

## 📋 Commandes Spéciales

| Commande | Description |
|----------|-------------|
| `:help` | Afficher l'aide complète |
| `:scan` | Scanner/rescanner le projet |
| `:files` | Lister tous les fichiers du workspace |
| `:auto on/off` | Activer/désactiver l'auto-approbation |
| `:model <nom>` | Changer de modèle AI |
| `:clear` | Effacer l'historique et le contexte |
| `:exit` ou `:quit` | Quitter l'agent |

## 🎯 Comment ça Fonctionne ?

### Détection d'Intention Automatique

L'agent analyse votre message et détecte :

**Mots-clés de modification** :
- crée, créer, create
- ajoute, ajouter, add
- modifie, modifier, change
- supprime, delete
- corrige, fix
- implémente, implement

**Mots-clés de lecture** :
- explique, explain
- analyse, analyze
- montre, show
- lis, read

**Conversation** :
- Tout le reste (questions, discussions, etc.)

### Système de Permissions

1. **Détection** : L'agent détecte qu'une modification est nécessaire
2. **Demande** : Affiche ce qui va être fait
3. **Choix utilisateur** :
   - `o` (oui) : Approuve cette fois
   - `n` (non) : Refuse la modification
   - `toujours` : Active l'auto-approve pour la session
4. **Exécution** : Si approuvé, utilise Aider pour modifier

## 📊 Workflow Typique

### Découverte d'un Nouveau Projet

```bash
# 1. Lancer l'agent
python3 scripts/claudine-smart.py

# 2. Scanner le projet (fait automatiquement au démarrage)
You> :scan

# 3. Poser des questions
You> Explique-moi ce que fait ce projet

# 4. Demander des améliorations
You> Comment puis-je améliorer la performance ?

# 5. Appliquer des modifications
You> Ajoute du caching à la fonction process_data
[Approuver]
```

### Développement Itératif

```bash
# 1. Créer une nouvelle fonctionnalité
You> Crée une classe User avec nom, email, et méthodes de validation
[Approuver]

# 2. Poser des questions sur ce qui a été créé
You> Est-ce que la validation d'email est sécurisée ?

# 3. Raffiner
You> Améliore la validation d'email avec regex
[Approuver]

# 4. Ajouter des tests
You> Crée des tests unitaires pour la classe User
[Approuver]
```

## 🔧 Configuration

### Modèle par Défaut

```bash
# Dans votre shell
export DEFAULT_MODEL=qwen2.5-coder:32b

# Ou dans l'agent
You> :model qwen2.5-coder:32b
```

### URL Ollama Custom

```bash
export OLLAMA_API_BASE=http://localhost:11434
```

## 💪 Avantages vs Autres Agents

| Fonctionnalité | Smart | Interactif | Aider | TUI |
|----------------|-------|------------|-------|-----|
| Conversation | ✅ | 🟡 Via API | ❌ | ✅ |
| Modification code | ✅ | ✅ | ✅ | ✅ |
| Permissions | ✅ | ❌ | ❌ | ❌ |
| Scan projet | ✅ | ❌ | 🟡 | ❌ |
| Détection auto | ✅ | ❌ | ❌ | ❌ |
| Réponses rapides | ✅ | 🟡 | ❌ | 🟡 |

## 🎓 Tips & Astuces

### 1. Commencer Large puis Précis

```
You> Analyse mon projet

[Comprend la structure]

You> Crée des tests pour le module auth

[Plus précis, meilleur résultat]
```

### 2. Utiliser :auto pour Prototypes Rapides

```
You> :auto on

You> Crée model User
You> Crée model Post
You> Crée model Comment
You> Crée les relations entre les models

[Tout se fait automatiquement]

You> :auto off
```

### 3. Poser des Questions Avant de Modifier

```
You> Comment devrais-je structurer mon API REST ?

[Obtenir des conseils]

You> OK, implémente cette structure

[Appliquer]
```

### 4. Scanner Après Modifications Externes

```bash
# Si vous avez modifié des fichiers manuellement
You> :scan

# L'agent mettra à jour sa compréhension du projet
```

## 🐛 Dépannage

### "Connection refused"

```bash
# Vérifier que les services tournent
make status

# Redémarrer si nécessaire
make restart
```

### Réponses Lentes

- Première requête toujours plus lente (chargement du modèle)
- Utilisez un modèle plus petit : `:model codellama:7b`
- Les conversations sont rapides (2-5s)
- Les modifications prennent plus de temps (20-40s)

### Modifications Non Détectées

Si l'agent crée un fichier au lieu de répondre :
- Reformulez votre question
- Exemple : ❌ "crée une explication de ..."
- Mieux : ✅ "explique-moi ..."

### Auto-Approve Trop Agressif

```
You> :auto off
```

Redemande permission à chaque fois.

## 📚 Comparaison avec Claude Code

| Fonctionnalité | Agent Smart | Claude Code |
|----------------|-------------|-------------|
| Local/Privé | ✅ | ❌ (cloud) |
| Gratuit | ✅ | ❌ |
| Permissions | ✅ | ✅ |
| Scan projet | ✅ | ✅ |
| Conversation | ✅ | ✅ |
| Modification code | ✅ | ✅ |
| Vitesse | 🟡 (20-40s) | 🟢 (5-15s) |
| Qualité | 🟢 | 🟢🟢 |

## 🔮 Futures Améliorations

- [ ] Streaming des réponses pour feedback immédiat
- [ ] Mémoire longue durée entre sessions
- [ ] Intégration avec IDE (VS Code extension)
- [ ] Support multi-fichiers simultanés
- [ ] Suggestions proactives

## 📖 Voir Aussi

- [CLI-AGENTS.md](CLI-AGENTS.md) - Comparaison des 4 agents
- [EXAMPLES.md](EXAMPLES.md) - Exemples d'utilisation avancés
- [README.md](README.md) - Documentation principale

---

**L'Agent Smart est votre assistant de code idéal : intelligent, respectueux, et toujours à votre service !** 🤖✨
