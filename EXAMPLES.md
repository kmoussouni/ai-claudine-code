# Exemples d'Utilisation

Ce document présente des exemples concrets d'utilisation de Claudine pour différents cas d'usage.

## 1. Génération de Code

### Créer une nouvelle fonction

```bash
python3 scripts/cli.py chat "Crée une fonction Python qui calcule le PGCD de deux nombres avec l'algorithme d'Euclide"
```

### Créer un fichier complet

```bash
python3 scripts/cli.py chat "Crée un fichier workspace/server.py contenant un serveur FastAPI avec :
- Un endpoint GET /health
- Un endpoint POST /users pour créer un utilisateur
- Validation des données avec Pydantic
- Gestion d'erreurs"
```

### Créer des tests

```bash
python3 scripts/cli.py chat "Crée des tests pytest pour toutes les fonctions" \
  --files workspace/math_utils.py
```

## 2. Modification de Code Existant

### Refactoring

```bash
python3 scripts/cli.py chat "Refactor cette fonction pour utiliser list comprehension et améliorer la lisibilité" \
  --files workspace/data_processor.py
```

### Ajout de fonctionnalités

```bash
python3 scripts/cli.py chat "Ajoute :
1. Validation des entrées
2. Gestion d'erreurs avec try/except
3. Logging des opérations
4. Type hints complets" \
  --files workspace/api.py
```

### Optimisation

```bash
python3 scripts/cli.py chat "Optimise cette fonction pour les performances. Identifie les bottlenecks et propose des améliorations" \
  --files workspace/data_processing.py
```

## 3. Debugging

### Identifier un bug

```bash
python3 scripts/cli.py chat "Analyse ce code et identifie pourquoi la fonction retourne None au lieu du résultat attendu" \
  --files workspace/buggy_function.py
```

### Ajouter du logging

```bash
python3 scripts/cli.py chat "Ajoute du logging détaillé pour debugger les problèmes de performance" \
  --files workspace/slow_process.py
```

## 4. Documentation

### Ajouter des docstrings

```bash
python3 scripts/cli.py chat "Ajoute des docstrings Google style à toutes les fonctions et classes" \
  --files workspace/module.py
```

### Générer un README

```bash
python3 scripts/cli.py chat "Analyse le code et génère un README.md avec :
- Description du projet
- Installation
- Usage avec exemples
- API documentation" \
  --files workspace/main.py workspace/api.py
```

## 5. Projets Web

### API REST

```bash
python3 scripts/cli.py chat "Crée une API REST complète pour gérer une bibliothèque :
- Modèles : Book, Author
- Endpoints CRUD complets
- SQLAlchemy pour la DB
- Authentification JWT
- Tests unitaires
Crée les fichiers nécessaires dans workspace/library-api/"
```

### Frontend React

```bash
python3 scripts/cli.py chat "Crée un composant React pour afficher une liste de tâches avec :
- Affichage des tâches
- Ajout de nouvelle tâche
- Marquage comme complété
- Suppression
- Utilise TypeScript et hooks"
```

## 6. Scripts d'Automatisation

### Script de backup

```bash
python3 scripts/cli.py chat "Crée un script Python qui :
- Sauvegarde une base de données PostgreSQL
- Compresse le fichier
- Upload sur S3
- Rotation automatique (garde seulement les 7 derniers)
- Notifications par email en cas d'erreur"
```

### Script de déploiement

```bash
python3 scripts/cli.py chat "Crée un script bash de déploiement qui :
- Pull le code depuis git
- Run les tests
- Build le projet
- Redémarre les services
- Rollback en cas d'erreur"
```

## 7. Data Science

### Analyse de données

```bash
python3 scripts/cli.py chat "Crée un notebook Jupyter qui analyse le dataset :
- Load le CSV
- Statistiques descriptives
- Visualisations (histogrammes, scatter plots)
- Détection d'outliers
- Corrélations entre variables" \
  --files workspace/data.csv
```

### Machine Learning

```bash
python3 scripts/cli.py chat "Crée un pipeline ML pour prédire les prix :
- Preprocessing des données
- Feature engineering
- Train/test split
- Entraînement de plusieurs modèles (Linear, Random Forest, XGBoost)
- Évaluation et comparaison
- Sauvegarde du meilleur modèle"
```

## 8. DevOps

### Dockerfile

```bash
python3 scripts/cli.py chat "Crée un Dockerfile multi-stage optimisé pour cette application Python FastAPI" \
  --files workspace/requirements.txt workspace/main.py
```

### Docker Compose

```bash
python3 scripts/cli.py chat "Crée un docker-compose.yml pour :
- App Python FastAPI
- PostgreSQL avec persistent volume
- Redis pour le cache
- Nginx comme reverse proxy
- Configuration réseau appropriée"
```

### CI/CD Pipeline

```bash
python3 scripts/cli.py chat "Crée un fichier .github/workflows/ci.yml qui :
- Run les tests sur push
- Check le linting
- Build Docker image
- Push sur Docker Hub si tests OK
- Deploy automatique sur staging"
```

## 9. Sécurité

### Code review sécurité

```bash
python3 scripts/cli.py chat "Analyse ce code pour identifier les vulnérabilités de sécurité :
- Injection SQL
- XSS
- CSRF
- Gestion des secrets
- Validation des entrées
Propose des corrections" \
  --files workspace/app.py
```

### Ajout d'authentification

```bash
python3 scripts/cli.py chat "Ajoute un système d'authentification JWT complet :
- Endpoints login/logout
- Middleware de vérification
- Refresh tokens
- Password hashing avec bcrypt" \
  --files workspace/api.py
```

## 10. Conversion de Code

### Python vers TypeScript

```bash
python3 scripts/cli.py chat "Convertis cette logique Python en TypeScript équivalent" \
  --files workspace/algorithm.py
```

### Refactoring vers Clean Architecture

```bash
python3 scripts/cli.py chat "Refactor ce code monolithique vers une Clean Architecture avec :
- Séparation domain/use-cases/adapters
- Injection de dépendances
- Interfaces pour les repositories" \
  --files workspace/monolith.py
```

## 11. Usage via API REST

### Avec curl

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Crée une fonction pour valider un email",
    "files": [],
    "model": "qwen2.5-coder:7b"
  }'
```

### Avec Python requests

```python
import requests

response = requests.post(
    "http://localhost:3000/chat",
    json={
        "message": "Explique comment optimiser cette boucle",
        "files": ["workspace/loop.py"],
        "model": "qwen2.5-coder:7b"
    }
)

result = response.json()
print(result["response"])
```

### Avec JavaScript/fetch

```javascript
const response = await fetch('http://localhost:3000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Ajoute la validation TypeScript',
    files: ['workspace/types.ts'],
    model: 'qwen2.5-coder:7b'
  })
});

const result = await response.json();
console.log(result.response);
```

## 12. Prompts Avancés

### Avec contexte multiple

```bash
python3 scripts/cli.py chat "Analyse l'architecture complète de cette app et propose des améliorations pour :
- Performance
- Sécurité
- Maintenabilité
- Scalabilité" \
  --files workspace/models.py workspace/api.py workspace/database.py workspace/config.py
```

### Génération de projet complet

```bash
python3 scripts/cli.py chat "Crée un projet de blog complet dans workspace/blog/ avec :

Backend (FastAPI) :
- Models : User, Post, Comment
- CRUD complet
- Auth JWT
- Tests pytest

Frontend (React + TypeScript) :
- Composants modulaires
- State management avec Context
- API client
- Routing

Infra :
- Docker compose
- PostgreSQL
- Nginx

Documentation :
- README avec setup
- API documentation
- Architecture diagram (text)"
```

## 13. Intégration Continue

### Dans un script de pre-commit

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Demander à Claudine de vérifier le code
python3 scripts/cli.py chat "Analyse les changements et vérifie :
- Pas de console.log oubliés
- Pas de TODO en production
- Code formatting correct
- Pas de secrets hardcodés" \
  --files $(git diff --cached --name-only)
```

## Tips pour de Meilleurs Résultats

### 1. Soyez spécifique

❌ Mauvais :
```bash
python3 scripts/cli.py chat "Améliore ce code"
```

✅ Bon :
```bash
python3 scripts/cli.py chat "Optimise cette fonction pour :
- Réduire la complexité temporelle de O(n²) à O(n log n)
- Utiliser moins de mémoire
- Ajouter du caching pour les appels répétés"
```

### 2. Donnez du contexte

```bash
python3 scripts/cli.py chat "Cette fonction fait partie d'une API REST qui traite 10000 requêtes/min.
Optimise-la pour réduire la latence. La priorité est la vitesse, pas la mémoire." \
  --files workspace/hot_path.py
```

### 3. Utilisez le bon modèle

- Tâches simples → `qwen2.5-coder:7b`
- Refactoring complexe → `qwen2.5-coder:32b`
- Code critique → `deepseek-coder-v2:16b`

```bash
python3 scripts/cli.py chat "Refactoring complexe..." \
  --model qwen2.5-coder:32b \
  --files workspace/complex.py
```

### 4. Itérez

```bash
# Première passe
python3 scripts/cli.py chat "Crée une classe User basique"

# Vérifiez le résultat, puis continuez
python3 scripts/cli.py chat "Ajoute validation des données et méthodes helper" \
  --files workspace/user.py

# Raffinez
python3 scripts/cli.py chat "Ajoute les tests unitaires" \
  --files workspace/user.py
```

---

Pour plus d'exemples, consultez le README.md et l'INTEGRATION.md
