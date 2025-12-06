"""
title: Generate Image with Stable Diffusion
author: Claudine
version: 1.0.0
description: Generate images using Stable Diffusion for game assets, illustrations, and more
"""

import requests
import json
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    """Open WebUI Function for image generation"""

    def __init__(self):
        self.valves = self.Valves()

    class Valves(BaseModel):
        """Configuration for the function"""
        AGENT_API_URL: str = Field(
            default="http://code-agent:3000",
            description="URL of the Claudine Agent API"
        )
        DEFAULT_STEPS: int = Field(
            default=20,
            description="Default number of diffusion steps"
        )
        DEFAULT_CFG_SCALE: float = Field(
            default=7.0,
            description="Default CFG scale"
        )

    async def generate_image(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        steps: Optional[int] = None,
        negative_prompt: Optional[str] = None,
        __user__: dict = {},
    ) -> str:
        """
        Generate an image using Stable Diffusion.

        Args:
            prompt: Description of the image to generate
            width: Image width (default: 512)
            height: Image height (default: 512)
            steps: Number of diffusion steps (default: 20)
            negative_prompt: What to avoid in the image

        Examples:
            - generate_image("pixel art knight character")
            - generate_image("magic sword with blue flames", width=256, height=256)
            - generate_image("forest background", negative_prompt="blurry, low quality")
        """

        try:
            # Préparer la requête
            payload = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "steps": steps or self.valves.DEFAULT_STEPS,
                "cfg_scale": self.valves.DEFAULT_CFG_SCALE,
                "save_to_disk": True
            }

            if negative_prompt:
                payload["negative_prompt"] = negative_prompt

            # Appeler l'API Agent
            response = requests.post(
                f"{self.valves.AGENT_API_URL}/generate-image",
                json=payload,
                timeout=300  # 5 minutes max
            )

            if response.status_code != 200:
                return f"❌ Error: {response.status_code} - {response.text}"

            result = response.json()

            # Formater la réponse
            output = f"""
🎨 **Image Generated Successfully!**

📝 **Prompt:** {result.get('prompt', prompt)}
📏 **Size:** {width}x{height}px
🎲 **Seed:** {result.get('seed', 'N/A')}
💾 **Saved to:** `{result.get('image_path', 'N/A')}`

The image has been generated and saved in the workspace.
To view it, check the `generated-images` folder.
"""

            return output.strip()

        except requests.Timeout:
            return "⏱️ Timeout: Image generation took too long (>5 minutes). Try with fewer steps or smaller size."
        except Exception as e:
            return f"❌ Error generating image: {str(e)}"
