#!/usr/bin/env python3
"""
Client CLI pour Claudine - Agent de code local
Permet d'interagir avec l'agent depuis la ligne de commande
"""

import sys
import argparse
import httpx
import json
from typing import List, Optional

API_BASE_URL = "http://localhost:3000"

def check_health():
    """Vérifie l'état de santé du système"""
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)
        data = response.json()
        print("🏥 État du système :")
        print(f"   API: {data['api']}")
        print(f"   Ollama: {data['ollama']}")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("   Assurez-vous que les services sont démarrés (./scripts/start.sh)")
        return False

def list_models():
    """Liste tous les modèles disponibles"""
    try:
        response = httpx.get(f"{API_BASE_URL}/models", timeout=10.0)
        data = response.json()
        print("📦 Modèles disponibles :")
        for model in data['models']:
            print(f"   - {model['name']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def chat(message: str, files: Optional[List[str]] = None, model: Optional[str] = None):
    """Envoie un message à l'agent"""
    try:
        payload = {
            "message": message,
            "files": files or [],
        }
        if model:
            payload["model"] = model

        print(f"💬 Envoi de la requête à l'agent...")
        print(f"   Message: {message}")
        if files:
            print(f"   Fichiers: {', '.join(files)}")

        response = httpx.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=300.0
        )

        data = response.json()
        print(f"\n📝 Réponse ({data['status']}):")
        print("=" * 60)
        print(data['response'])
        print("=" * 60)

    except httpx.TimeoutException:
        print("⏱️  Timeout: l'opération a pris trop de temps")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def list_workspace_files():
    """Liste les fichiers dans le workspace"""
    try:
        response = httpx.get(f"{API_BASE_URL}/workspace/files", timeout=10.0)
        data = response.json()
        print("📁 Fichiers dans le workspace :")
        for file in data['files']:
            print(f"   - {file}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Claudine CLI - Agent de code local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Vérifier l'état du système
  %(prog)s health

  # Lister les modèles disponibles
  %(prog)s models

  # Demander à l'agent de créer un fichier
  %(prog)s chat "Crée un fichier hello.py qui affiche Hello World"

  # Modifier un fichier existant
  %(prog)s chat "Ajoute une fonction pour calculer la factorielle" --files math_utils.py

  # Utiliser un modèle spécifique
  %(prog)s chat "Explique ce code" --model qwen2.5-coder:32b --files app.py

  # Lister les fichiers du workspace
  %(prog)s files
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')

    # Commande health
    subparsers.add_parser('health', help='Vérifier l\'état du système')

    # Commande models
    subparsers.add_parser('models', help='Lister les modèles disponibles')

    # Commande chat
    chat_parser = subparsers.add_parser('chat', help='Envoyer un message à l\'agent')
    chat_parser.add_argument('message', help='Message à envoyer')
    chat_parser.add_argument('--files', nargs='+', help='Fichiers à modifier (relatifs au workspace)')
    chat_parser.add_argument('--model', help='Modèle à utiliser')

    # Commande files
    subparsers.add_parser('files', help='Lister les fichiers du workspace')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'health':
        check_health()
    elif args.command == 'models':
        list_models()
    elif args.command == 'chat':
        chat(args.message, args.files, args.model)
    elif args.command == 'files':
        list_workspace_files()

if __name__ == "__main__":
    main()
