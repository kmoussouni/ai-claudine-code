"""
Service de génération d'images via ComfyUI + FLUX
Remplace Stable Diffusion par FLUX pour une meilleure qualité
"""

import httpx
import json
import uuid
import asyncio
from typing import Optional, Dict, Any
from pathlib import Path


class FluxGenerator:
    """Service de génération d'images via ComfyUI + FLUX"""

    def __init__(
        self,
        comfyui_url: str = "http://flux-comfyui:8188",
        output_dir: str = "/workspace/generated-images"
    ):
        self.comfyui_url = comfyui_url
        self.output_dir = Path(output_dir)
        self.client = httpx.AsyncClient(timeout=300.0)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def check_health(self) -> bool:
        """Vérifie si ComfyUI est disponible"""
        try:
            response = await self.client.get(f"{self.comfyui_url}/system_stats")
            return response.status_code == 200
        except Exception:
            return False

    def create_flux_workflow(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        steps: int = 4,
        seed: int = -1,
        model: str = "flux1-schnell"
    ) -> Dict:
        """
        Crée un workflow ComfyUI pour FLUX

        FLUX.1-schnell : 4 steps (rapide)
        FLUX.1-dev : 20-30 steps (qualité)
        """

        if seed == -1:
            seed = int(uuid.uuid4().int % (2**32))

        # Workflow ComfyUI simplifié pour FLUX
        workflow = {
            "1": {  # CLIP Text Encode (prompt)
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": ["11", 0]
                }
            },
            "2": {  # Empty Latent Image
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                }
            },
            "3": {  # KSampler (génération)
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": 1.0,  # FLUX utilise CFG=1
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "denoise": 1.0,
                    "model": ["10", 0],
                    "positive": ["1", 0],
                    "negative": ["6", 0],
                    "latent_image": ["2", 0]
                }
            },
            "6": {  # Negative prompt (vide pour FLUX)
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "",
                    "clip": ["11", 0]
                }
            },
            "8": {  # VAE Decode
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["12", 0]
                }
            },
            "9": {  # Save Image
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "flux",
                    "images": ["8", 0]
                }
            },
            "10": {  # Load Checkpoint
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": f"{model}.safetensors"
                }
            },
            "11": {  # CLIP from checkpoint
                "class_type": "CLIPLoader",
                "inputs": {
                    "clip_name": "clip_l.safetensors"
                }
            },
            "12": {  # VAE Loader
                "class_type": "VAELoader",
                "inputs": {
                    "vae_name": "ae.safetensors"
                }
            }
        }

        return workflow

    async def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        steps: int = 4,
        seed: int = -1,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Génère une image via ComfyUI + FLUX

        Args:
            prompt: Description de l'image
            width: Largeur (recommandé: 1024 pour FLUX)
            height: Hauteur (recommandé: 1024 pour FLUX)
            steps: Nombre de steps (4 pour schnell, 20-30 pour dev)
            seed: Seed aléatoire
            model_name: "flux1-schnell" (rapide) ou "flux1-dev" (qualité)
        """

        model = model_name or "flux1-schnell"

        # Créer le workflow
        workflow = self.create_flux_workflow(
            prompt=prompt,
            width=width,
            height=height,
            steps=steps,
            seed=seed,
            model=model
        )

        try:
            # Envoyer le workflow à ComfyUI
            prompt_id = str(uuid.uuid4())

            response = await self.client.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow, "client_id": prompt_id}
            )

            if response.status_code != 200:
                raise Exception(f"ComfyUI error: {response.status_code}")

            result = response.json()

            # Attendre que l'image soit générée
            await self._wait_for_completion(prompt_id)

            # Récupérer l'image
            image_path = await self._get_output_image(prompt_id)

            return {
                "image_path": str(image_path) if image_path else None,
                "seed": seed,
                "prompt": prompt,
                "model": model,
                "info": {
                    "width": width,
                    "height": height,
                    "steps": steps,
                    "model": model
                }
            }

        except Exception as e:
            raise Exception(f"Erreur génération FLUX: {str(e)}")

    async def _wait_for_completion(self, prompt_id: str, max_wait: int = 300):
        """Attend que la génération soit terminée"""
        for _ in range(max_wait):
            try:
                response = await self.client.get(f"{self.comfyui_url}/history/{prompt_id}")
                if response.status_code == 200:
                    history = response.json()
                    if prompt_id in history:
                        return
            except:
                pass
            await asyncio.sleep(1)

        raise Exception("Timeout: génération trop longue")

    async def _get_output_image(self, prompt_id: str) -> Optional[Path]:
        """Récupère l'image générée"""
        try:
            response = await self.client.get(f"{self.comfyui_url}/history/{prompt_id}")
            history = response.json()

            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_output in outputs.values():
                    if "images" in node_output:
                        image_info = node_output["images"][0]
                        filename = image_info["filename"]

                        # Télécharger l'image
                        image_response = await self.client.get(
                            f"{self.comfyui_url}/view",
                            params={"filename": filename, "type": "output"}
                        )

                        # Sauvegarder dans workspace
                        output_path = self.output_dir / filename
                        with open(output_path, "wb") as f:
                            f.write(image_response.content)

                        return output_path
        except Exception as e:
            print(f"Erreur récupération image: {e}")

        return None

    async def close(self):
        """Ferme la connexion HTTP"""
        await self.client.aclose()
