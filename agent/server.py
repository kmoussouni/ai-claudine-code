#!/usr/bin/env python3
"""
Serveur API pour l'agent de code Claudine
Fournit une interface REST pour interagir avec Aider et les modèles locaux
"""

import os
import subprocess
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx

app = FastAPI(
    title="Claudine Code Agent API",
    description="API pour agent de code avec modèles AI locaux",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:7b")
WORKSPACE_DIR = "/workspace"

# Modèles de données
class ChatRequest(BaseModel):
    message: str
    files: Optional[List[str]] = []
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str

class ModelInfo(BaseModel):
    name: str
    size: Optional[str] = None
    available: bool

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "service": "Claudine Code Agent",
        "status": "running",
        "ollama_url": OLLAMA_BASE_URL,
        "default_model": DEFAULT_MODEL
    }

@app.get("/health")
async def health():
    """Vérification de l'état de santé"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            ollama_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        ollama_status = f"unhealthy: {str(e)}"

    return {
        "api": "healthy",
        "ollama": ollama_status
    }

@app.get("/models")
async def list_models():
    """Liste tous les modèles disponibles dans Ollama"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [
                    ModelInfo(
                        name=model.get("name"),
                        size=model.get("size"),
                        available=True
                    )
                    for model in data.get("models", [])
                ]
                return {"models": models}
            else:
                raise HTTPException(status_code=500, detail="Impossible de récupérer les modèles")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Envoie un message à l'agent de code
    Le message peut inclure des fichiers à modifier
    """
    model = request.model or DEFAULT_MODEL

    try:
        # Construction de la commande Aider
        cmd = [
            "aider",
            "--model", f"ollama/{model}",
            "--yes-always",  # Auto-accepte les changements
            "--message", request.message
        ]

        # Ajout des fichiers si spécifiés
        if request.files:
            for file in request.files:
                file_path = os.path.join(WORKSPACE_DIR, file)
                if os.path.exists(file_path):
                    cmd.append(file_path)

        # Préparer l'environnement pour Aider
        env = os.environ.copy()
        env['OLLAMA_API_BASE'] = OLLAMA_BASE_URL

        # Exécution dans le workspace
        result = subprocess.run(
            cmd,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            env=env,
            timeout=300  # 5 minutes timeout
        )

        return ChatResponse(
            response=result.stdout + result.stderr,
            status="success" if result.returncode == 0 else "error"
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Timeout: l'opération a pris trop de temps")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ollama/pull/{model_name}")
async def pull_model(model_name: str):
    """Télécharge un nouveau modèle"""
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/pull",
                json={"name": model_name}
            )
            return {"status": "success", "model": model_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workspace/files")
async def list_workspace_files():
    """Liste les fichiers dans le workspace"""
    try:
        files = []
        for root, dirs, filenames in os.walk(WORKSPACE_DIR):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, WORKSPACE_DIR)
                files.append(rel_path)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
