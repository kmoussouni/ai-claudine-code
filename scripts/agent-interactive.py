#!/usr/bin/env python3
"""
Claudine Interactive CLI Agent
Agent de code conversationnel interactif
"""

import sys
import os
import httpx
import json
from pathlib import Path
from typing import List, Optional
import readline  # Pour l'historique de commandes

# Configuration
API_BASE_URL = os.getenv("CLAUDINE_API_URL", "http://localhost:3000")
WORKSPACE_DIR = Path("workspace")
HISTORY_FILE = Path.home() / ".claudine_history"

# Couleurs ANSI
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ClaudineAgent:
    def __init__(self):
        self.client = httpx.Client(timeout=300.0)
        self.current_files: List[str] = []
        self.current_model = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:7b")
        self.conversation_history = []

        # Charger l'historique des commandes
        if HISTORY_FILE.exists():
            readline.read_history_file(HISTORY_FILE)
        readline.set_history_length(1000)

    def print_banner(self):
        """Affiche la bannière de démarrage"""
        print(f"{Colors.OKBLUE}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              Claudine - Agent CLI Interactif             ║")
        print("║                  Agent de Code Local                     ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Modèle actuel: {self.current_model}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Workspace: {WORKSPACE_DIR.absolute()}{Colors.ENDC}")
        print()
        print(f"{Colors.WARNING}Commandes spéciales:{Colors.ENDC}")
        print("  :help          - Afficher l'aide")
        print("  :model <nom>   - Changer de modèle")
        print("  :files [...]   - Définir les fichiers de contexte")
        print("  :clear         - Effacer le contexte")
        print("  :history       - Afficher l'historique")
        print("  :workspace     - Lister les fichiers du workspace")
        print("  :exit / :quit  - Quitter")
        print()

    def check_health(self) -> bool:
        """Vérifie la connexion au serveur"""
        try:
            response = self.client.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("api") == "healthy":
                    return True
            return False
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erreur de connexion: {e}{Colors.ENDC}")
            print(f"{Colors.WARNING}Assurez-vous que les services sont démarrés: make start{Colors.ENDC}")
            return False

    def send_message(self, message: str) -> Optional[str]:
        """Envoie un message à l'agent"""
        try:
            payload = {
                "message": message,
                "files": self.current_files,
                "model": self.current_model
            }

            print(f"\n{Colors.OKCYAN}🤖 Agent réfléchit...{Colors.ENDC}")

            response = self.client.post(
                f"{API_BASE_URL}/chat",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                self.conversation_history.append({
                    "user": message,
                    "agent": data["response"]
                })
                return data["response"]
            else:
                return f"{Colors.FAIL}Erreur {response.status_code}: {response.text}{Colors.ENDC}"

        except httpx.TimeoutException:
            return f"{Colors.FAIL}⏱️  Timeout: l'opération a pris trop de temps{Colors.ENDC}"
        except Exception as e:
            return f"{Colors.FAIL}❌ Erreur: {e}{Colors.ENDC}"

    def handle_command(self, command: str) -> bool:
        """Gère les commandes spéciales. Retourne True pour continuer, False pour quitter"""

        if command in [":exit", ":quit", ":q"]:
            print(f"{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
            return False

        elif command == ":help":
            self.print_banner()

        elif command.startswith(":model"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                self.current_model = parts[1]
                print(f"{Colors.OKGREEN}✓ Modèle changé: {self.current_model}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}Usage: :model <nom-du-modele>{Colors.ENDC}")

        elif command.startswith(":files"):
            parts = command.split()[1:]
            if parts:
                self.current_files = parts
                print(f"{Colors.OKGREEN}✓ Fichiers de contexte: {', '.join(self.current_files)}{Colors.ENDC}")
            else:
                self.current_files = []
                print(f"{Colors.WARNING}Contexte de fichiers effacé{Colors.ENDC}")

        elif command == ":clear":
            self.current_files = []
            self.conversation_history = []
            print(f"{Colors.OKGREEN}✓ Contexte et historique effacés{Colors.ENDC}")

        elif command == ":history":
            if not self.conversation_history:
                print(f"{Colors.WARNING}Aucun historique{Colors.ENDC}")
            else:
                print(f"\n{Colors.BOLD}📜 Historique de la conversation:{Colors.ENDC}\n")
                for i, exchange in enumerate(self.conversation_history, 1):
                    print(f"{Colors.OKBLUE}[{i}] Vous:{Colors.ENDC}")
                    print(f"    {exchange['user'][:100]}...")
                    print(f"{Colors.OKGREEN}    Agent:{Colors.ENDC}")
                    print(f"    {exchange['agent'][:100]}...")
                    print()

        elif command == ":workspace":
            print(f"\n{Colors.BOLD}📁 Fichiers dans le workspace:{Colors.ENDC}\n")
            try:
                response = self.client.get(f"{API_BASE_URL}/workspace/files")
                if response.status_code == 200:
                    files = response.json().get("files", [])
                    if files:
                        for f in sorted(files):
                            print(f"  {Colors.OKCYAN}•{Colors.ENDC} {f}")
                    else:
                        print(f"  {Colors.WARNING}(vide){Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}Erreur lors de la récupération des fichiers{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}Erreur: {e}{Colors.ENDC}")
            print()

        else:
            print(f"{Colors.FAIL}❌ Commande inconnue: {command}{Colors.ENDC}")
            print(f"{Colors.WARNING}Tapez :help pour voir les commandes disponibles{Colors.ENDC}")

        return True

    def run(self):
        """Boucle principale de l'agent"""
        self.print_banner()

        # Vérifier la connexion
        if not self.check_health():
            return

        print(f"{Colors.OKGREEN}✓ Connecté au serveur Claudine{Colors.ENDC}\n")

        try:
            while True:
                # Prompt avec contexte
                context_info = ""
                if self.current_files:
                    context_info = f" [{len(self.current_files)} fichiers]"

                prompt = f"{Colors.BOLD}You{context_info}>{Colors.ENDC} "

                try:
                    user_input = input(prompt).strip()
                except EOFError:
                    print()
                    break

                if not user_input:
                    continue

                # Commande spéciale
                if user_input.startswith(":"):
                    if not self.handle_command(user_input):
                        break
                    continue

                # Message normal à l'agent
                response = self.send_message(user_input)
                if response:
                    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Agent>{Colors.ENDC}")
                    print(f"{response}")
                    print()

        except KeyboardInterrupt:
            print(f"\n\n{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
        finally:
            # Sauvegarder l'historique
            try:
                readline.write_history_file(HISTORY_FILE)
            except:
                pass
            self.client.close()

def main():
    agent = ClaudineAgent()
    agent.run()

if __name__ == "__main__":
    main()
