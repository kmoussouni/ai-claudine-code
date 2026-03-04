"""
title: Generate Image with FLUX
author: Claudine
version: 2.0.0
description: Generate images using FLUX via ComfyUI. Ask the AI to generate an image and it will call this tool automatically.
"""

import requests
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    """Open WebUI Tool for image generation via FLUX/ComfyUI"""

    def __init__(self):
        self.valves = self.Valves()

    class Valves(BaseModel):
        AGENT_API_URL: str = Field(
            default="http://code-agent:3000",
            description="URL of the Claudine Agent API"
        )
        DEFAULT_WIDTH: int = Field(default=1024, description="Default image width")
        DEFAULT_HEIGHT: int = Field(default=1024, description="Default image height")
        DEFAULT_STEPS: int = Field(default=4, description="Steps (4=schnell rapide, 20-30=dev qualité)")
        DEFAULT_MODEL: str = Field(default="flux1-schnell", description="flux1-schnell ou flux1-dev")

    def generate_image(
        self,
        prompt: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = None,
        model: Optional[str] = None,
        __user__: dict = {},
    ) -> str:
        """
        Generate an image using FLUX AI model.
        Call this tool whenever the user asks to generate, create, or draw an image.

        Args:
            prompt: Detailed description of the image to generate (English works best)
            width: Image width in pixels (default: 1024, FLUX native resolution)
            height: Image height in pixels (default: 1024)
            steps: Diffusion steps — 4 for speed (schnell), 20-30 for quality (dev)
            model: "flux1-schnell" (fast, Apache 2.0) or "flux1-dev" (quality, non-commercial)

        Examples:
            generate_image("a cute cat sitting on a window sill, golden hour lighting")
            generate_image("pixel art knight character, blue armor", width=512, height=512)
            generate_image("fantasy landscape, mountains and lake", width=1024, height=576)
        """
        payload = {
            "prompt": prompt,
            "width": width or self.valves.DEFAULT_WIDTH,
            "height": height or self.valves.DEFAULT_HEIGHT,
            "steps": steps or self.valves.DEFAULT_STEPS,
            "model_name": model or self.valves.DEFAULT_MODEL,
            "save_to_disk": True,
        }

        try:
            response = requests.post(
                f"{self.valves.AGENT_API_URL}/generate-image",
                json=payload,
                timeout=600,
            )

            if response.status_code == 503:
                return "⚠️ FLUX n'est pas disponible. Vérifiez que le service est démarré (`make start`) et que les modèles sont téléchargés."

            if response.status_code != 200:
                return f"❌ Erreur {response.status_code} : {response.text[:300]}"

            result = response.json()
            image_path = result.get("image_path", "N/A")

            # Construire le chemin relatif pour l'affichage WebUI
            # Les images sont montées dans /app/backend/static/generated-images/
            filename = image_path.split("/")[-1] if image_path else "unknown"
            webui_url = f"/generated-images/{filename}"

            return (
                f"🎨 **Image générée avec succès !**\n\n"
                f"**Prompt :** {result.get('prompt', prompt)}\n"
                f"**Taille :** {payload['width']}×{payload['height']}px\n"
                f"**Modèle :** {payload['model_name']} ({payload['steps']} steps)\n"
                f"**Seed :** {result.get('seed', 'N/A')}\n\n"
                f"![Image générée]({webui_url})"
            )

        except requests.Timeout:
            return "⏱️ Timeout : la génération a pris trop longtemps (>10 min). Essayez avec moins de steps ou une résolution plus petite."
        except requests.ConnectionError:
            return "❌ Impossible de joindre l'agent API. Vérifiez que les services Docker sont démarrés (`make start`)."
        except Exception as exc:
            return f"❌ Erreur : {exc}"
