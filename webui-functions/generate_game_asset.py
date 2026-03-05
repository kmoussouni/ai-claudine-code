"""
title: Generate Game Asset
author: Claudine
version: 1.0.0
description: Generate game assets (icons, items, backgrounds, characters, tilesets)
"""

import requests
import json
from typing import Optional, Literal
from pydantic import BaseModel, Field


class Tools:
    """Open WebUI Function for game asset generation"""

    def __init__(self):
        self.valves = self.Valves()

    class Valves(BaseModel):
        """Configuration for the function"""
        AGENT_API_URL: str = Field(
            default="http://code-agent:3000",
            description="URL of the Claudine Agent API"
        )
        DEFAULT_STEPS: int = Field(
            default=25,
            description="Default number of diffusion steps for assets"
        )

    async def generate_game_asset(
        self,
        asset_type: Literal["icon", "item", "background", "character", "tileset"],
        description: str,
        size: int = 512,
        steps: Optional[int] = None,
        negative_prompt: Optional[str] = None,
        __user__: dict = {},
    ) -> str:
        """
        Generate a game asset (icon, item, background, character, or tileset).

        Args:
            asset_type: Type of asset to generate (icon, item, background, character, tileset)
            description: Description of the asset
            size: Size of the square image (default: 512)
            steps: Number of diffusion steps (default: 25)
            negative_prompt: What to avoid in the asset

        Examples:
            - generate_game_asset("item", "magic sword with blue flames")
            - generate_game_asset("icon", "health potion red liquid", size=256)
            - generate_game_asset("background", "medieval castle interior")
            - generate_game_asset("character", "knight in full armor front view")
            - generate_game_asset("tileset", "grass and stone tiles seamless")
        """

        # Validation du type
        valid_types = ["icon", "item", "background", "character", "tileset"]
        if asset_type not in valid_types:
            return f"❌ Invalid asset type. Must be one of: {', '.join(valid_types)}"

        try:
            # Préparer la requête
            payload = {
                "asset_type": asset_type,
                "description": description,
                "size": size,
                "steps": steps or self.valves.DEFAULT_STEPS,
            }

            if negative_prompt:
                payload["negative_prompt"] = negative_prompt

            # Appeler l'API Agent
            response = requests.post(
                f"{self.valves.AGENT_API_URL}/generate-game-asset",
                json=payload,
                timeout=300
            )

            if response.status_code != 200:
                return f"❌ Error: {response.status_code} - {response.text}"

            result = response.json()

            # Emojis par type d'asset
            asset_emojis = {
                "icon": "🎯",
                "item": "⚔️",
                "background": "🏞️",
                "character": "👤",
                "tileset": "🧩"
            }

            emoji = asset_emojis.get(asset_type, "🎨")

            # Formater la réponse
            output = f"""
{emoji} **Game Asset Generated Successfully!**

📦 **Type:** {asset_type.capitalize()}
📝 **Description:** {result.get('prompt', description)}
📏 **Size:** {size}x{size}px
🎲 **Seed:** {result.get('seed', 'N/A')}
💾 **Saved to:** `{result.get('image_path', 'N/A')}`

**Tips for using in your game:**
"""

            # Conseils spécifiques par type
            if asset_type == "icon":
                output += """
- Perfect for UI elements and inventory icons
- Consider creating variants (selected, disabled, etc.)
- Use consistent size across all icons
"""
            elif asset_type == "item":
                output += """
- Great for inventory systems and loot drops
- Can be used as-is or as reference for pixel art
- Consider adding glow/outline for rarity tiers
"""
            elif asset_type == "background":
                output += """
- Can be used as parallax layers
- May need seamless tiling adjustments
- Consider color grading for different times of day
"""
            elif asset_type == "character":
                output += """
- Use as concept art or sprite reference
- May need multiple views (front, side, back)
- Can be basis for creating sprite sheets
"""
            elif asset_type == "tileset":
                output += """
- Check if tiles are seamlessly tileable
- May need manual adjustments for perfect tiling
- Create variations for visual diversity
"""

            return output.strip()

        except requests.Timeout:
            return "⏱️ Timeout: Asset generation took too long. Try with fewer steps."
        except Exception as e:
            return f"❌ Error generating asset: {str(e)}"
