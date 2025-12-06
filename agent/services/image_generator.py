"""
Service de génération d'images via Stable Diffusion
Intègre l'API Stable Diffusion WebUI pour générer des images, spritesheets et assets de jeux
"""

import httpx
import base64
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path


class ImageGenerator:
    """Service de génération d'images via Stable Diffusion API"""

    def __init__(
        self,
        sd_url: str = None,
        output_dir: str = "/workspace/generated-images",
        default_steps: int = 20,
        default_cfg_scale: float = 7.0
    ):
        self.sd_url = sd_url or os.getenv("SD_API_URL", "http://stable-diffusion:7860")
        self.output_dir = Path(output_dir)
        self.default_steps = default_steps
        self.default_cfg_scale = default_cfg_scale
        self.client = httpx.AsyncClient(timeout=300.0)

        # Créer le dossier de sortie s'il n'existe pas
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def check_health(self) -> bool:
        """Vérifie si le service Stable Diffusion est disponible"""
        try:
            response = await self.client.get(f"{self.sd_url}/sdapi/v1/sd-models")
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> List[Dict[str, Any]]:
        """Liste tous les modèles Stable Diffusion disponibles"""
        try:
            response = await self.client.get(f"{self.sd_url}/sdapi/v1/sd-models")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        seed: int = -1,
        sampler_name: str = "DPM++ 2M Karras",
        save_to_disk: bool = True
    ) -> Dict[str, Any]:
        """
        Génère une image via Stable Diffusion API

        Args:
            prompt: Description de l'image à générer
            negative_prompt: Ce qu'on ne veut PAS dans l'image
            width: Largeur de l'image
            height: Hauteur de l'image
            steps: Nombre d'étapes de diffusion
            cfg_scale: Échelle CFG (créativité vs fidélité au prompt)
            seed: Seed aléatoire (-1 = aléatoire)
            sampler_name: Algorithme de sampling
            save_to_disk: Sauvegarder l'image dans workspace

        Returns:
            Dict avec image_path, image_base64, seed, info
        """

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt or "blurry, bad quality, distorted, low resolution",
            "width": width,
            "height": height,
            "steps": steps or self.default_steps,
            "cfg_scale": cfg_scale or self.default_cfg_scale,
            "seed": seed,
            "sampler_name": sampler_name,
        }

        try:
            response = await self.client.post(
                f"{self.sd_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=300.0
            )

            if response.status_code != 200:
                raise Exception(f"SD API error: {response.status_code} - {response.text}")

            result = response.json()

            # L'image est en base64 dans result['images'][0]
            image_base64 = result['images'][0]
            info = result.get('info', {})

            # Parser l'info JSON si c'est une string
            if isinstance(info, str):
                import json
                try:
                    info = json.loads(info)
                except:
                    info = {}

            image_path = None
            if save_to_disk:
                image_path = await self._save_image(image_base64, prompt, info.get('seed', seed))

            return {
                "image_path": str(image_path) if image_path else None,
                "image_base64": image_base64,
                "seed": info.get('seed', seed),
                "info": info,
                "prompt": prompt,
                "negative_prompt": negative_prompt
            }

        except httpx.TimeoutException:
            raise Exception("Timeout: la génération d'image a pris trop de temps (>5 min)")
        except Exception as e:
            raise Exception(f"Erreur génération image: {str(e)}")

    async def generate_spritesheet(
        self,
        prompt: str,
        frames: int = 4,
        frame_width: int = 64,
        frame_height: int = 64,
        negative_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère un spritesheet pour jeu vidéo

        Args:
            prompt: Description du sprite (ex: "knight character walking")
            frames: Nombre de frames dans le spritesheet
            frame_width: Largeur d'une frame
            frame_height: Hauteur d'une frame
            **kwargs: Arguments additionnels pour generate_image

        Returns:
            Dict avec le spritesheet généré
        """

        # Adapter le prompt pour spritesheet
        spritesheet_prompt = (
            f"{prompt}, sprite sheet, {frames} frames, "
            f"game asset, pixel art style, animation frames, "
            f"side view, transparent background, consistent style"
        )

        # Negative prompt adapté pour spritesheets
        sprite_negative = (
            "blurry, distorted, inconsistent, different styles, "
            "3d render, realistic, photo, bad anatomy"
        )
        if negative_prompt:
            sprite_negative = f"{sprite_negative}, {negative_prompt}"

        # Calculer dimensions totales
        width = frame_width * frames
        height = frame_height

        return await self.generate_image(
            prompt=spritesheet_prompt,
            negative_prompt=sprite_negative,
            width=width,
            height=height,
            steps=kwargs.get('steps', 30),  # Plus de steps pour meilleure qualité
            cfg_scale=kwargs.get('cfg_scale', 7.5),
            **{k: v for k, v in kwargs.items() if k not in ['steps', 'cfg_scale']}
        )

    async def generate_game_asset(
        self,
        asset_type: str,
        description: str,
        size: int = 512,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère un asset de jeu (icon, item, background, etc.)

        Args:
            asset_type: Type d'asset (icon, item, background, character, tileset)
            description: Description de l'asset
            size: Taille de l'image (carré)
            **kwargs: Arguments additionnels

        Returns:
            Dict avec l'asset généré
        """

        asset_prompts = {
            "icon": "game icon, pixel art, {desc}, item icon, 16x16 style, centered, simple background",
            "item": "game item, {desc}, pixel art, RPG style, detailed, isometric view",
            "background": "game background, {desc}, 2D game art, seamless, environment",
            "character": "game character, {desc}, sprite art, full body, standing pose",
            "tileset": "tileset, {desc}, seamless tiles, game asset, repeatable pattern"
        }

        prompt_template = asset_prompts.get(asset_type, "game asset, {desc}, pixel art style")
        full_prompt = prompt_template.format(desc=description)

        return await self.generate_image(
            prompt=full_prompt,
            width=size,
            height=size,
            **kwargs
        )

    async def _save_image(
        self,
        image_base64: str,
        prompt: str,
        seed: int
    ) -> Path:
        """
        Sauvegarde une image sur le disque

        Args:
            image_base64: Image encodée en base64
            prompt: Prompt utilisé (pour le nom de fichier)
            seed: Seed utilisé

        Returns:
            Path vers le fichier sauvegardé
        """
        import base64

        # Décoder l'image
        image_data = base64.b64decode(image_base64)

        # Créer nom de fichier avec timestamp et hash du prompt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]

        filename = f"{timestamp}_{prompt_hash}_seed{seed}.png"
        filepath = self.output_dir / filename

        # Sauvegarder
        with open(filepath, 'wb') as f:
            f.write(image_data)

        return filepath

    async def close(self):
        """Ferme la connexion HTTP"""
        await self.client.aclose()
