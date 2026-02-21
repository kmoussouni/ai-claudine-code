# Contribuer à Claudine

Merci de votre intérêt pour contribuer à Claudine ! Ce document explique comment contribuer au projet.

## Code de Conduite

En participant à ce projet, vous acceptez de maintenir un environnement respectueux et inclusif pour tous.

## Comment Contribuer

### 1. Reporter des Bugs

Si vous trouvez un bug :

1. Vérifiez qu'il n'a pas déjà été reporté dans les Issues
2. Créez une nouvelle Issue avec :
   - Titre clair et descriptif
   - Description détaillée du problème
   - Steps pour reproduire
   - Comportement attendu vs actuel
   - Version de Claudine
   - Logs pertinents

### 2. Proposer des Fonctionnalités

Pour proposer une nouvelle fonctionnalité :

1. Créez une Issue avec le tag "enhancement"
2. Décrivez :
   - Le problème que ça résout
   - Comment ça devrait fonctionner
   - Pourquoi c'est important
3. Attendez les retours avant de commencer le développement

### 3. Soumettre des Pull Requests

#### Setup Environnement de Développement

```bash
# Fork et clone le repo
git clone https://github.com/votre-username/claudine.git
cd claudine

# Créer une branche
git checkout -b feature/ma-fonctionnalite

# Installer et tester
./scripts/setup.sh
make start
```

#### Guidelines de Code

**Python**
- Suivre PEP 8
- Type hints obligatoires
- Docstrings Google style
- Tests pour nouvelle fonctionnalité

**Shell Scripts**
- Utiliser `set -e` en début de fichier
- Commenter les sections importantes
- Gérer les erreurs proprement

**Docker**
- Images multi-stage si possible
- Minimiser les layers
- Ne pas hardcoder de secrets

#### Process de PR

1. **Créer une branche**
   ```bash
   git checkout -b feature/nom-descriptif
   ```

2. **Faire vos modifications**
   - Code clair et commenté
   - Tests si applicable
   - Mise à jour de la documentation

3. **Tester localement**
   ```bash
   # Vérifier que tout fonctionne
   make stop
   make build
   make start
   make status

   # Tester votre fonctionnalité
   python3 scripts/cli.py health
   ```

4. **Commit avec message clair**
   ```bash
   git add .
   git commit -m "feat: ajoute support pour modèle llama3.2

   - Ajoute configuration pour llama3.2
   - Met à jour documentation
   - Ajoute tests"
   ```

   Format des messages de commit :
   - `feat:` Nouvelle fonctionnalité
   - `fix:` Correction de bug
   - `docs:` Documentation uniquement
   - `refactor:` Refactoring de code
   - `test:` Ajout de tests
   - `chore:` Tâches de maintenance

5. **Push et créer PR**
   ```bash
   git push origin feature/nom-descriptif
   ```

   Puis créer la PR sur GitHub avec :
   - Description claire de ce qui change
   - Pourquoi ce changement
   - Comment tester
   - Screenshots si UI

6. **Review**
   - Attendez les reviews
   - Adressez les commentaires
   - Mettez à jour si nécessaire

### 4. Améliorer la Documentation

La documentation est toujours la bienvenue !

- Corriger des typos
- Clarifier des sections confuses
- Ajouter des exemples
- Traduire (futurs languages)

Fichiers documentation :
- `README.md` - Documentation principale
- `INTEGRATION.md` - Intégrations IDE
- `EXAMPLES.md` - Exemples d'usage
- `CONTRIBUTING.md` - Ce fichier

## Domaines qui Nécessitent de l'Aide

### Haute Priorité

- **Tests** : Ajouter des tests automatisés
- **Documentation** : Plus d'exemples d'utilisation
- **Performance** : Optimisations du serveur API
- **Support modèles** : Ajouter support pour plus de modèles

### Moyenne Priorité

- **UI/UX** : Améliorer l'interface web
- **CLI** : Ajouter plus de commandes
- **Monitoring** : Métriques et observabilité
- **Sécurité** : Audit et améliorations

### Basse Priorité

- **Intégrations** : Plus d'éditeurs/IDEs
- **Plugins** : Système de plugins
- **Localisation** : Support multilingue

## Structure du Code

```
claudine/
├── agent/                  # Service agent de code
│   ├── server.py          # API FastAPI principale
│   ├── Dockerfile         # Image Docker agent
│   └── config/            # Configuration agent
├── workspace/             # Espace de travail partagé
├── scripts/               # Scripts utilitaires
│   ├── setup.sh          # Installation
│   ├── start.sh          # Démarrage
│   ├── stop.sh           # Arrêt
│   ├── pull-model.sh     # Téléchargement modèles
│   └── cli.py            # Client CLI Python
├── docker-compose.yml    # Orchestration services
├── Makefile              # Commandes simplifiées
└── docs/                 # Documentation
```

## Guidelines Techniques

### API REST (FastAPI)

- Utiliser les modèles Pydantic pour validation
- Documenter les endpoints avec docstrings
- Gérer les erreurs proprement (HTTPException)
- Timeout appropriés pour long-running tasks
- Logging pour debugging

### Docker

- Images Alpine ou slim quand possible
- Multi-stage builds pour réduire la taille
- Health checks dans docker-compose
- Volumes pour data persistante
- Networks appropriés

### Scripts Shell

- Shebang : `#!/bin/bash`
- Set options : `set -e` (exit on error)
- Variables en majuscules
- Fonctions pour code réutilisable
- Messages clairs pour l'utilisateur

### Python

```python
# Type hints
def process_data(input_data: List[str]) -> Dict[str, Any]:
    """Process input data and return results.

    Args:
        input_data: List of strings to process

    Returns:
        Dictionary containing processed results

    Raises:
        ValueError: If input_data is empty
    """
    pass

# Gestion d'erreurs
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Failed: {e}")
    raise
```

## Tests

### Ajouter des Tests

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from agent.server import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert "api" in response.json()

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "test", "files": []}
    )
    assert response.status_code == 200
```

### Lancer les Tests

```bash
# Installation des dépendances de test
pip install pytest pytest-cov httpx

# Lancer les tests
pytest

# Avec coverage
pytest --cov=agent --cov-report=html
```

## Documentation API

L'API FastAPI génère automatiquement la documentation :
- Swagger UI : http://localhost:3000/docs
- ReDoc : http://localhost:3000/redoc

Assurez-vous que vos endpoints sont bien documentés :

```python
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Envoie un message à l'agent de code.

    Le message peut inclure des fichiers à modifier.
    L'agent retournera le code modifié ou créé.

    Args:
        request: Requête contenant le message et les fichiers

    Returns:
        Réponse de l'agent avec le code généré

    Raises:
        HTTPException: Si l'opération échoue
    """
    pass
```

## Processus de Release

1. **Bump version** dans `version.txt`
2. **Update CHANGELOG.md**
3. **Créer tag git**
   ```bash
   git tag -a v1.2.0 -m "Release 1.2.0"
   git push origin v1.2.0
   ```
4. **Créer GitHub Release**
5. **Build et push images Docker** (si applicable)

## Support et Questions

- **Issues GitHub** : Pour bugs et features
- **Discussions** : Pour questions générales
- **Documentation** : Consulter README et docs/

## Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT, la même que le projet.

## Remerciements

Merci à tous les contributeurs qui aident à améliorer Claudine ! 🙏

---

Des questions ? N'hésitez pas à ouvrir une Discussion ou Issue sur GitHub.
