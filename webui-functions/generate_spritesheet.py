"""
title: Generate Spritesheet
author: Claudine
version: 1.0.0
description: Generate spritesheets for game development with multiple animation frames
"""

import requests
import json
from typing import Optional
from pydantic import BaseModel, Field


class Tools:
    """Open WebUI Function for spritesheet generation"""

    def __init__(self):
        self.valves = self.Valves()

    class Valves(BaseModel):
        """Configuration for the function"""
        AGENT_API_URL: str = Field(
            default="http://code-agent:3000",
            description="URL of the Claudine Agent API"
        )
        DEFAULT_STEPS: int = Field(
            default=30,
            description="Default number of diffusion steps for spritesheets"
        )

    async def generate_spritesheet(
        self,
        prompt: str,
        frames: int = 4,
        frame_width: int = 64,
        frame_height: int = 64,
        steps: Optional[int] = None,
        negative_prompt: Optional[str] = None,
        __user__: dict = {},
    ) -> str:
        """
        Generate a spritesheet for game development.

        Args:
            prompt: Description of the sprite (e.g., "knight walking")
            frames: Number of animation frames (default: 4)
            frame_width: Width of each frame in pixels (default: 64)
            frame_height: Height of each frame in pixels (default: 64)
            steps: Number of diffusion steps (default: 30)
            negative_prompt: What to avoid in the spritesheet

        Examples:
            - generate_spritesheet("knight walking animation")
            - generate_spritesheet("player character running", frames=8, frame_width=32)
            - generate_spritesheet("enemy slime idle animation", frames=6)
        """

        try:
            # Préparer la requête
            payload = {
                "prompt": prompt,
                "frames": frames,
                "frame_width": frame_width,
                "frame_height": frame_height,
                "steps": steps or self.valves.DEFAULT_STEPS,
            }

            if negative_prompt:
                payload["negative_prompt"] = negative_prompt

            # Appeler l'API Agent
            response = requests.post(
                f"{self.valves.AGENT_API_URL}/generate-spritesheet",
                json=payload,
                timeout=300
            )

            if response.status_code != 200:
                return f"❌ Error: {response.status_code} - {response.text}"

            result = response.json()

            # Calculer dimensions totales
            total_width = frame_width * frames

            # Formater la réponse
            output = f"""
🎮 **Spritesheet Generated Successfully!**

📝 **Description:** {result.get('prompt', prompt)}
🎞️ **Frames:** {frames} frames
📏 **Frame Size:** {frame_width}x{frame_height}px
📐 **Total Size:** {total_width}x{frame_height}px
🎲 **Seed:** {result.get('seed', 'N/A')}
💾 **Saved to:** `{result.get('image_path', 'N/A')}`

**Usage in Unity:**
1. Import the spritesheet into your Unity project
2. Set Texture Type to "Sprite (2D and UI)"
3. Set Sprite Mode to "Multiple"
4. Open Sprite Editor and slice into {frames} frames ({frame_width}x{frame_height} each)
5. Create an animation using the frames
"""

            return output.strip()

        except requests.Timeout:
            return "⏱️ Timeout: Spritesheet generation took too long. Try with fewer frames or smaller size."
        except Exception as e:
            return f"❌ Error generating spritesheet: {str(e)}"
