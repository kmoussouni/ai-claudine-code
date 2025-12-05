#!/usr/bin/env python3
"""
Claudine Smart Agent - Agent Hybride Intelligent
Combine conversation et modification de code avec système de permissions
"""

import sys
import os
import httpx
import json
import subprocess
import glob
from pathlib import Path
from typing import List, Optional, Dict
import readline

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:7b")
WORKSPACE_DIR = Path("workspace")
HISTORY_FILE = Path.home() / ".claudine_smart_history"

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
    DIM = '\033[2m'

class SmartAgent:
    def __init__(self):
        self.client = httpx.Client(timeout=120.0)
        self.current_model = DEFAULT_MODEL
        self.conversation_history = []
        self.project_context = {}
        self.auto_approve = False

        # Charger l'historique
        if HISTORY_FILE.exists():
            readline.read_history_file(HISTORY_FILE)
        readline.set_history_length(1000)

    def print_banner(self):
        """Affiche la bannière"""
        print(f"{Colors.OKBLUE}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║         Claudine Smart - Agent Hybride Intelligent       ║")
        print("║    Conversation + Modification de Code avec Permission   ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Modèle: {self.current_model}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Workspace: {WORKSPACE_DIR.absolute()}{Colors.ENDC}")
        print()
        print(f"{Colors.WARNING}Commandes spéciales:{Colors.ENDC}")
        print("  :help          - Afficher l'aide")
        print("  :scan          - Scanner le projet")
        print("  :files         - Lister les fichiers du workspace")
        print("  :auto [on/off] - Activer/désactiver auto-approve")
        print("  :model <nom>   - Changer de modèle")
        print("  :clear         - Effacer l'historique")
        print("  :exit / :quit  - Quitter")
        print()

    def check_ollama(self) -> bool:
        """Vérifie la connexion à Ollama"""
        try:
            response = self.client.get(f"{OLLAMA_URL}/api/tags")
            return response.status_code == 200
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erreur de connexion à Ollama: {e}{Colors.ENDC}")
            print(f"{Colors.WARNING}Assurez-vous que les services sont démarrés: make start{Colors.ENDC}")
            return False

    def scan_project(self) -> Dict:
        """Scanne le projet pour comprendre sa structure"""
        print(f"{Colors.OKCYAN}🔍 Scan du projet...{Colors.ENDC}")

        context = {
            "files": [],
            "languages": set(),
            "structure": {}
        }

        if not WORKSPACE_DIR.exists():
            print(f"{Colors.WARNING}Le workspace est vide{Colors.ENDC}")
            return context

        # Parcourir les fichiers
        for file_path in WORKSPACE_DIR.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(WORKSPACE_DIR)
                context["files"].append(str(rel_path))

                # Détecter les langages
                ext = file_path.suffix
                if ext:
                    context["languages"].add(ext)

        self.project_context = context

        print(f"{Colors.OKGREEN}✓ {len(context['files'])} fichiers trouvés{Colors.ENDC}")
        if context["languages"]:
            print(f"{Colors.DIM}  Langages détectés: {', '.join(sorted(context['languages']))}{Colors.ENDC}")

        return context

    def chat_with_ollama(self, message: str, system_prompt: str = None) -> str:
        """Chat direct avec Ollama"""
        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # Ajouter le contexte du projet si disponible
            if self.project_context.get("files"):
                context_msg = f"Contexte du projet: {len(self.project_context['files'])} fichiers"
                if self.project_context.get("languages"):
                    context_msg += f", langages: {', '.join(self.project_context['languages'])}"
                messages.append({
                    "role": "system",
                    "content": context_msg
                })

            messages.append({
                "role": "user",
                "content": message
            })

            response = self.client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": self.current_model,
                    "messages": messages,
                    "stream": False
                }
            )

            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return f"Erreur {response.status_code}"

        except Exception as e:
            return f"Erreur: {e}"

    def analyze_intent(self, message: str) -> Dict:
        """Analyse l'intention de l'utilisateur"""

        # Mots-clés pour modifications de code
        code_keywords = [
            "crée", "créer", "create", "ajoute", "ajouter", "add",
            "modifie", "modifier", "modify", "change", "refactor",
            "supprime", "supprimer", "delete", "remove",
            "corrige", "corriger", "fix", "bug",
            "implémente", "implémenter", "implement"
        ]

        # Mots-clés pour lecture/analyse
        read_keywords = [
            "explique", "expliquer", "explain",
            "analyse", "analyser", "analyze",
            "montre", "montrer", "show",
            "lis", "lire", "read",
            "qu'est-ce", "c'est quoi", "what is"
        ]

        message_lower = message.lower()

        # Détection
        needs_code_change = any(keyword in message_lower for keyword in code_keywords)
        needs_read = any(keyword in message_lower for keyword in read_keywords)

        return {
            "needs_code_change": needs_code_change,
            "needs_read": needs_read,
            "is_conversational": not (needs_code_change or needs_read)
        }

    def ask_permission(self, action: str) -> bool:
        """Demande permission à l'utilisateur"""
        if self.auto_approve:
            print(f"{Colors.DIM}(Auto-approuvé){Colors.ENDC}")
            return True

        print(f"\n{Colors.WARNING}⚠️  Permission requise:{Colors.ENDC}")
        print(f"{Colors.BOLD}{action}{Colors.ENDC}")

        while True:
            response = input(f"{Colors.OKCYAN}Approuver? [o/N/toujours] :{Colors.ENDC} ").strip().lower()

            if response in ['o', 'oui', 'y', 'yes']:
                return True
            elif response in ['toujours', 'always', 'a']:
                self.auto_approve = True
                print(f"{Colors.OKGREEN}✓ Auto-approve activé pour cette session{Colors.ENDC}")
                return True
            elif response in ['n', 'non', 'no', '']:
                return False
            else:
                print(f"{Colors.FAIL}Réponse invalide. Utilisez o/n/toujours{Colors.ENDC}")

    def execute_code_change(self, message: str) -> str:
        """Exécute une modification de code avec Aider"""

        # Demander permission
        if not self.ask_permission(f"Modifier le code: {message}"):
            return f"{Colors.WARNING}❌ Modification annulée par l'utilisateur{Colors.ENDC}"

        print(f"{Colors.OKCYAN}🔧 Exécution de la modification...{Colors.ENDC}")

        try:
            # Préparer l'environnement
            env = os.environ.copy()
            env['OLLAMA_API_BASE'] = OLLAMA_URL

            # Commande Aider
            cmd = [
                "aider",
                "--model", f"ollama/{self.current_model}",
                "--yes-always",
                "--message", message
            ]

            # Exécuter dans le workspace
            result = subprocess.run(
                cmd,
                cwd=WORKSPACE_DIR,
                capture_output=True,
                text=True,
                env=env,
                timeout=120
            )

            return result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return f"{Colors.FAIL}⏱️  Timeout{Colors.ENDC}"
        except Exception as e:
            return f"{Colors.FAIL}❌ Erreur: {e}{Colors.ENDC}"

    def read_file(self, filepath: str) -> str:
        """Lit un fichier du workspace"""
        try:
            full_path = WORKSPACE_DIR / filepath
            if not full_path.exists():
                return f"Fichier non trouvé: {filepath}"

            with open(full_path, 'r') as f:
                content = f.read()

            return content
        except Exception as e:
            return f"Erreur lecture: {e}"

    def handle_message(self, message: str) -> str:
        """Traite un message de l'utilisateur"""

        # Analyser l'intention
        intent = self.analyze_intent(message)

        # Si c'est une modification de code
        if intent["needs_code_change"]:
            return self.execute_code_change(message)

        # Si c'est une lecture de fichier spécifique
        if "fichier" in message.lower() or "file" in message.lower():
            # Demander à Ollama d'abord pour comprendre
            pass

        # Conversation normale
        return self.chat_with_ollama(message)

    def handle_command(self, command: str) -> bool:
        """Gère les commandes spéciales"""

        if command in [":exit", ":quit", ":q"]:
            print(f"{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
            return False

        elif command == ":help":
            self.print_banner()

        elif command == ":scan":
            self.scan_project()

        elif command == ":files":
            if not self.project_context.get("files"):
                self.scan_project()

            print(f"\n{Colors.BOLD}📁 Fichiers du workspace:{Colors.ENDC}\n")
            for f in sorted(self.project_context.get("files", [])):
                print(f"  {Colors.OKCYAN}•{Colors.ENDC} {f}")
            print()

        elif command.startswith(":auto"):
            parts = command.split()
            if len(parts) > 1:
                if parts[1] in ["on", "oui", "yes"]:
                    self.auto_approve = True
                    print(f"{Colors.OKGREEN}✓ Auto-approve activé{Colors.ENDC}")
                else:
                    self.auto_approve = False
                    print(f"{Colors.WARNING}✓ Auto-approve désactivé{Colors.ENDC}")
            else:
                status = "activé" if self.auto_approve else "désactivé"
                print(f"Auto-approve: {status}")

        elif command.startswith(":model"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                self.current_model = parts[1]
                print(f"{Colors.OKGREEN}✓ Modèle: {self.current_model}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}Usage: :model <nom>{Colors.ENDC}")

        elif command == ":clear":
            self.conversation_history = []
            self.project_context = {}
            print(f"{Colors.OKGREEN}✓ Contexte effacé{Colors.ENDC}")

        else:
            print(f"{Colors.FAIL}❌ Commande inconnue: {command}{Colors.ENDC}")
            print(f"{Colors.WARNING}Tapez :help pour l'aide{Colors.ENDC}")

        return True

    def run(self):
        """Boucle principale"""
        self.print_banner()

        # Vérifier Ollama
        if not self.check_ollama():
            return

        print(f"{Colors.OKGREEN}✓ Connecté à Ollama{Colors.ENDC}\n")

        # Scanner le projet automatiquement
        self.scan_project()
        print()

        try:
            while True:
                # Prompt
                auto_status = f"{Colors.DIM}[auto]{Colors.ENDC} " if self.auto_approve else ""
                prompt = f"{auto_status}{Colors.BOLD}You>{Colors.ENDC} "

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

                # Message normal
                print(f"\n{Colors.OKCYAN}🤖 Claudine réfléchit...{Colors.ENDC}\n")

                response = self.handle_message(user_input)

                print(f"{Colors.OKGREEN}{Colors.BOLD}Claudine>{Colors.ENDC}")
                print(response)
                print()

                # Sauvegarder dans l'historique
                self.conversation_history.append({
                    "user": user_input,
                    "assistant": response
                })

        except KeyboardInterrupt:
            print(f"\n\n{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
        finally:
            try:
                readline.write_history_file(HISTORY_FILE)
            except:
                pass
            self.client.close()

def main():
    agent = SmartAgent()
    agent.run()

if __name__ == "__main__":
    main()
