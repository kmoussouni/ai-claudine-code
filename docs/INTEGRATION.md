# Intégrations IDE

Ce guide explique comment intégrer Claudine avec différents éditeurs de code et IDEs.

## VS Code avec Continue

### Installation

1. Installer l'extension Continue depuis le marketplace VS Code
2. Ouvrir les paramètres Continue (Cmd/Ctrl + Shift + P → "Continue: Open config.json")
3. Copier le contenu de `config.continue.json` dans votre configuration

### Configuration Rapide

```bash
# Copier la config vers Continue
cp config.continue.json ~/.continue/config.json
```

### Utilisation

- `Cmd/Ctrl + L` : Ouvrir le chat Continue
- `Cmd/Ctrl + I` : Modifier le code avec l'AI
- Sélectionner du code + `Cmd/Ctrl + Shift + L` : Poser une question sur le code

### Commandes Personnalisées

Continue est configuré avec ces commandes :
- `/test` - Générer des tests unitaires
- `/optimize` - Optimiser le code
- `/explain` - Expliquer le code
- `/comment` - Ajouter des commentaires

## VS Code avec Extension Ollama

### Installation

1. Installer l'extension "Ollama" depuis le marketplace
2. Configurer l'URL : `http://localhost:11434`
3. Sélectionner le modèle dans la liste

## JetBrains IDEs (IntelliJ, PyCharm, WebStorm)

### Installation

1. Installer le plugin "Continue" depuis le marketplace JetBrains
2. Configurer dans Settings → Tools → Continue
3. Copier la configuration depuis `config.continue.json`

## Cursor

Cursor peut utiliser Ollama directement :

### Configuration

1. Ouvrir Cursor Settings
2. Aller dans "AI" ou "Models"
3. Ajouter un custom model :
   - API URL: `http://localhost:11434`
   - Model: `qwen2.5-coder:7b`
   - Provider: Ollama

## Neovim

### Avec copilot.lua

```lua
require('copilot').setup({
  suggestion = {
    auto_trigger = true,
  },
  server_opts_overrides = {
    settings = {
      http = {
        proxy = "http://localhost:11434",
      },
    },
  },
})
```

### Avec ChatGPT.nvim

```lua
require("chatgpt").setup({
  api_host_cmd = "http://localhost:11434",
  api_key_cmd = "echo ''",
  openai_params = {
    model = "qwen2.5-coder:7b",
  },
})
```

## Emacs avec GPTel

```elisp
(use-package gptel
  :config
  (setq gptel-model "qwen2.5-coder:7b"
        gptel-backend (gptel-make-ollama "Claudine"
                        :host "localhost:11434"
                        :stream t
                        :models '("qwen2.5-coder:7b"
                                 "qwen2.5-coder:32b"
                                 "codellama:7b"))))
```

## API REST Directe

Pour créer votre propre intégration :

### Endpoints Disponibles

```bash
# Santé du système
GET http://localhost:3000/health

# Lister les modèles
GET http://localhost:3000/models

# Chat avec l'agent
POST http://localhost:3000/chat
Content-Type: application/json

{
  "message": "Crée une fonction fibonacci",
  "files": ["workspace/math.py"],
  "model": "qwen2.5-coder:7b"
}

# Documentation interactive
GET http://localhost:3000/docs
```

### Exemple Python

```python
import httpx

def ask_claudine(message: str, files: list = None):
    response = httpx.post(
        "http://localhost:3000/chat",
        json={
            "message": message,
            "files": files or [],
            "model": "qwen2.5-coder:7b"
        },
        timeout=300.0
    )
    return response.json()

# Usage
result = ask_claudine(
    "Ajoute la gestion d'erreurs",
    files=["app.py"]
)
print(result["response"])
```

### Exemple JavaScript/TypeScript

```typescript
async function askClaudine(message: string, files: string[] = []) {
  const response = await fetch('http://localhost:3000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      files,
      model: 'qwen2.5-coder:7b'
    })
  });

  return await response.json();
}

// Usage
const result = await askClaudine(
  'Crée un composant React',
  ['src/App.tsx']
);
console.log(result.response);
```

## Ollama API Directe

Vous pouvez aussi utiliser l'API Ollama directement :

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b",
  "prompt": "Écris une fonction qui calcule fibonacci en Python",
  "stream": false
}'
```

## Troubleshooting

### Extension Continue ne se connecte pas

Vérifiez que :
1. Les services sont démarrés : `make status`
2. Ollama est accessible : `curl http://localhost:11434/api/tags`
3. Le modèle est téléchargé : `make models`

### Performances lentes dans l'IDE

- Utilisez un modèle plus petit (7B au lieu de 32B)
- Désactivez l'autocomplétion automatique
- Augmentez le timeout dans la config

### Le modèle n'apparaît pas dans Continue

```bash
# Vérifier que le modèle est bien installé
docker-compose exec ollama ollama list

# Redémarrer Continue
# Cmd/Ctrl + Shift + P → "Developer: Reload Window"
```

## Recommandations

### Pour l'autocomplétion rapide
- Utilisez `qwen2.5-coder:7b` (rapide et efficace)
- Activez le streaming

### Pour l'analyse de code complexe
- Utilisez `qwen2.5-coder:32b` ou `deepseek-coder-v2:16b`
- Donnez plus de contexte dans vos prompts

### Pour les refactorings importants
- Utilisez l'API REST avec plus de timeout
- Passez plusieurs fichiers en contexte
- Vérifiez les changements avant de les accepter

---

Pour plus d'informations, consultez le README.md principal.
