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

# Import services
from services.image_generator import ImageGenerator

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
SD_ENABLED = os.getenv("SD_ENABLED", "true").lower() == "true"
SD_API_URL = os.getenv("SD_API_URL", "http://stable-diffusion:7860")

# Initialiser le service de génération d'images
image_gen = ImageGenerator(sd_url=SD_API_URL) if SD_ENABLED else None

# Modèles de données - Code
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

# Modèles de données - Images
class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    steps: Optional[int] = None
    cfg_scale: Optional[float] = None
    seed: int = -1
    sampler_name: str = "DPM++ 2M Karras"
    save_to_disk: bool = True

class SpritesheetRequest(BaseModel):
    prompt: str
    frames: int = 4
    frame_width: int = 64
    frame_height: int = 64
    negative_prompt: Optional[str] = None
    steps: Optional[int] = None
    cfg_scale: Optional[float] = None
    seed: int = -1

class GameAssetRequest(BaseModel):
    asset_type: str  # icon, item, background, character, tileset
    description: str
    size: int = 512
    negative_prompt: Optional[str] = None
    steps: Optional[int] = None
    cfg_scale: Optional[float] = None

class ImageResponse(BaseModel):
    status: str
    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    seed: int
    prompt: str
    info: Optional[dict] = None

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

# ============================================================================
# Endpoints de génération d'images (Stable Diffusion)
# ============================================================================

@app.get("/sd/health")
async def sd_health():
    """Vérifie l'état de santé du service Stable Diffusion"""
    if not SD_ENABLED or not image_gen:
        return {"status": "disabled", "message": "Stable Diffusion n'est pas activé"}

    is_healthy = await image_gen.check_health()
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "url": SD_API_URL,
        "enabled": SD_ENABLED
    }

@app.get("/sd/models")
async def sd_models():
    """Liste les modèles Stable Diffusion disponibles"""
    if not SD_ENABLED or not image_gen:
        raise HTTPException(status_code=503, detail="Stable Diffusion n'est pas activé")

    try:
        models = await image_gen.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-image", response_model=ImageResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Génère une image via Stable Diffusion

    Exemple:
    ```
    {
        "prompt": "pixel art character, knight with blue armor",
        "negative_prompt": "blurry, bad quality",
        "width": 512,
        "height": 512,
        "steps": 20,
        "cfg_scale": 7.0
    }
    ```
    """
    if not SD_ENABLED or not image_gen:
        raise HTTPException(status_code=503, detail="Stable Diffusion n'est pas activé")

    try:
        result = await image_gen.generate_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            cfg_scale=request.cfg_scale,
            seed=request.seed,
            sampler_name=request.sampler_name,
            save_to_disk=request.save_to_disk
        )

        return ImageResponse(
            status="success",
            image_path=result.get("image_path"),
            image_base64=result.get("image_base64") if not request.save_to_disk else None,
            seed=result.get("seed"),
            prompt=result.get("prompt"),
            info=result.get("info")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération image: {str(e)}")

@app.post("/generate-spritesheet", response_model=ImageResponse)
async def generate_spritesheet(request: SpritesheetRequest):
    """
    Génère un spritesheet pour jeu vidéo

    Exemple:
    ```
    {
        "prompt": "knight character walking animation",
        "frames": 8,
        "frame_width": 64,
        "frame_height": 64,
        "steps": 30
    }
    ```
    """
    if not SD_ENABLED or not image_gen:
        raise HTTPException(status_code=503, detail="Stable Diffusion n'est pas activé")

    try:
        result = await image_gen.generate_spritesheet(
            prompt=request.prompt,
            frames=request.frames,
            frame_width=request.frame_width,
            frame_height=request.frame_height,
            negative_prompt=request.negative_prompt,
            steps=request.steps,
            cfg_scale=request.cfg_scale,
            seed=request.seed
        )

        return ImageResponse(
            status="success",
            image_path=result.get("image_path"),
            seed=result.get("seed"),
            prompt=result.get("prompt"),
            info=result.get("info")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération spritesheet: {str(e)}")

@app.post("/generate-game-asset", response_model=ImageResponse)
async def generate_game_asset(request: GameAssetRequest):
    """
    Génère un asset de jeu (icon, item, background, etc.)

    Types disponibles: icon, item, background, character, tileset

    Exemple:
    ```
    {
        "asset_type": "item",
        "description": "magic sword with blue flames",
        "size": 512,
        "steps": 25
    }
    ```
    """
    if not SD_ENABLED or not image_gen:
        raise HTTPException(status_code=503, detail="Stable Diffusion n'est pas activé")

    valid_types = ["icon", "item", "background", "character", "tileset"]
    if request.asset_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Type d'asset invalide. Utilisez: {', '.join(valid_types)}"
        )

    try:
        result = await image_gen.generate_game_asset(
            asset_type=request.asset_type,
            description=request.description,
            size=request.size,
            negative_prompt=request.negative_prompt,
            steps=request.steps,
            cfg_scale=request.cfg_scale
        )

        return ImageResponse(
            status="success",
            image_path=result.get("image_path"),
            seed=result.get("seed"),
            prompt=result.get("prompt"),
            info=result.get("info")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération asset: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
