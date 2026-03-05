#!/usr/bin/env python3
"""
Script CLI simple pour générer des images
Usage: python3 generate-image-cli.py "votre prompt"
"""

import sys
import requests
import json

# Configuration
API_URL = "http://localhost:3000"  # Changer par l'IP Windows si besoin

def generate_image(prompt, model="v1.5", quality="fast"):
    """Génère une image via l'API"""

    # Configuration selon le modèle
    configs = {
        "fast": {
            "width": 512,
            "height": 512,
            "steps": 20,
            "model_name": None  # v1.5 par défaut
        },
        "quality": {
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "model_name": "sd_xl_base_1.0"
        }
    }

    config = configs.get(quality, configs["fast"])

    payload = {
        "prompt": prompt,
        **config
    }

    print(f"\n🎨 Génération de l'image...")
    print(f"   Prompt: {prompt}")
    print(f"   Modèle: {'SDXL' if quality == 'quality' else 'SD v1.5'}")
    print(f"   Taille: {config['width']}x{config['height']}")
    print(f"   Steps: {config['steps']}\n")

    try:
        response = requests.post(
            f"{API_URL}/generate-image",
            json=payload,
            timeout=300
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Image générée avec succès !")
            print(f"   📁 Fichier: {result.get('image_path')}")
            print(f"   🎲 Seed: {result.get('seed')}")
            return result
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return None

    except requests.ConnectionError:
        print(f"❌ Impossible de se connecter à {API_URL}")
        print(f"   Vérifiez que Docker est démarré : docker-compose up -d")
        return None
    except requests.Timeout:
        print(f"⏱️  Timeout : la génération a pris trop de temps")
        return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 generate-image-cli.py 'votre prompt'")
        print("  python3 generate-image-cli.py 'votre prompt' --quality")
        print()
        print("Exemples:")
        print("  python3 generate-image-cli.py 'pixel art knight with blue armor'")
        print("  python3 generate-image-cli.py 'grandmother in JoJo style' --quality")
        sys.exit(1)

    prompt = sys.argv[1]
    quality = "quality" if "--quality" in sys.argv else "fast"

    generate_image(prompt, quality=quality)
