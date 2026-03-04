#!/usr/bin/env python3
"""
Claudine Smart Agent - Agent Hybride Intelligent
Combine conversation et modification de code avec système de permissions
"""

import os
import subprocess
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional
import readline
import httpx

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:7b")
WORKSPACE_DIR = Path("workspace")
HISTORY_FILE = Path.home() / ".claudine_smart_history"
STACK_PRESETS = {
    "php": {
        "model": os.getenv("PHP_MODEL", DEFAULT_MODEL),
        "instructions": "Generate modern PHP 8.x code following PSR-12; prefer Composer autoloading and clear separation of concerns."
    },
    "unity": {
        "model": os.getenv("UNITY_MODEL", DEFAULT_MODEL),
        "instructions": "Write Unity C# scripts targeting the current LTS; use MonoBehaviour patterns (Awake/Start/Update) and serialize fields when helpful."
    },
    "js": {
        "model": os.getenv("JS_MODEL", DEFAULT_MODEL),
        "instructions": "Produce modern JavaScript (ES2020+); default to ESM modules and keep side effects minimal."
    },
    "react": {
        "model": os.getenv("REACT_MODEL", DEFAULT_MODEL),
        "instructions": "Write React function components with hooks; favor composition over inheritance and keep components pure."
    },
    "bash": {
        "model": os.getenv("BASH_MODEL", DEFAULT_MODEL),
        "instructions": "Produce POSIX-friendly Bash; when generating scripts include set -euo pipefail and avoid unnecessary subshells."
    },
    "python": {
        "model": os.getenv("PY_MODEL", DEFAULT_MODEL),
        "instructions": "Generate Python 3.10+ code with type hints and clear separation of IO and logic; prefer pathlib over os.path."
    }
}


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
        self.project_context: Dict = {}
        self.auto_approve = False
        self.current_stack: Optional[str] = None
        self.stack_prompt: Optional[str] = None

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
        if self.current_stack:
            print(f"{Colors.OKCYAN}Stack: {self.current_stack}{Colors.ENDC}")
        print()
        print(f"{Colors.WARNING}Commandes spéciales:{Colors.ENDC}")
        print("  :help          - Afficher l'aide")
        print("  :scan          - Scanner le projet")
        print("  :files         - Lister les fichiers du workspace")
        print("  :status        - git status condensé")
        print("  :review        - Revue de code sur le diff courant")
        print("  :commit <msg>  - git add -A && git commit -m <msg>")
        print("  :auto [on/off] - Activer/désactiver auto-approve")
        print("  :model <nom>   - Changer de modèle")
        print("  :stack <nom>   - Préset langage (php, unity, js, react, bash, python)")
        print("  :clear         - Effacer l'historique")
        print("  :exit / :quit  - Quitter")
        print()

    def check_ollama(self) -> bool:
        """Vérifie la connexion à Ollama"""
        try:
            response = self.client.get(f"{OLLAMA_URL}/api/tags")
            return response.status_code == 200
        except Exception as exc:
            print(f"{Colors.FAIL}❌ Erreur de connexion à Ollama: {exc}{Colors.ENDC}")
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

                ext = file_path.suffix
                if ext:
                    context["languages"].add(ext)

        self.project_context = context

        print(f"{Colors.OKGREEN}✓ {len(context['files'])} fichiers trouvés{Colors.ENDC}")
        if context["languages"]:
            print(f"{Colors.DIM}  Langages détectés: {', '.join(sorted(context['languages']))}{Colors.ENDC}")

        return context

    def chat_with_ollama(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Chat direct avec Ollama"""
        try:
            messages: List[Dict[str, str]] = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            if self.stack_prompt:
                messages.append({"role": "system", "content": self.stack_prompt})

            if self.project_context.get("files"):
                context_msg = f"Contexte du projet: {len(self.project_context['files'])} fichiers"
                if self.project_context.get("languages"):
                    context_msg += f", langages: {', '.join(self.project_context['languages'])}"
                messages.append({"role": "system", "content": context_msg})

            messages.append({"role": "user", "content": message})

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
            return f"Erreur {response.status_code}: {response.text}"

        except Exception as exc:
            return f"Erreur: {exc}"

    def analyze_intent(self, message: str) -> Dict:
        """Analyse l'intention de l'utilisateur"""

        code_keywords = [
            "crée", "créer", "create", "ajoute", "ajouter", "add",
            "modifie", "modifier", "modify", "change", "refactor",
            "supprime", "supprimer", "delete", "remove",
            "corrige", "corriger", "fix", "bug",
            "implémente", "implémenter", "implement"
        ]

        read_keywords = [
            "explique", "expliquer", "explain",
            "analyse", "analyser", "analyze",
            "montre", "montrer", "show",
            "lis", "lire", "read",
            "qu'est-ce", "c'est quoi", "what is"
        ]

        message_lower = message.lower()
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
            if response in ['toujours', 'always', 'a']:
                self.auto_approve = True
                print(f"{Colors.OKGREEN}✓ Auto-approve activé pour cette session{Colors.ENDC}")
                return True
            if response in ['n', 'non', 'no', '']:
                return False
            print(f"{Colors.FAIL}Réponse invalide. Utilisez o/n/toujours{Colors.ENDC}")

    def execute_code_change(self, message: str) -> str:
        """Exécute une modification de code avec Aider"""

        if not self.ask_permission(f"Modifier le code: {message}"):
            return f"{Colors.WARNING}❌ Modification annulée par l'utilisateur{Colors.ENDC}"

        print(f"{Colors.OKCYAN}🔧 Exécution de la modification...{Colors.ENDC}")

        try:
            env = os.environ.copy()
            env['OLLAMA_API_BASE'] = OLLAMA_URL

            final_message = message
            if self.stack_prompt:
                final_message = f"{self.stack_prompt}\n\n{message}"

            cmd = [
                "aider",
                "--model", f"ollama/{self.current_model}",
                "--yes-always",
                "--message", final_message
            ]

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
        except Exception as exc:
            return f"{Colors.FAIL}❌ Erreur: {exc}{Colors.ENDC}"

    def read_file(self, filepath: str) -> str:
        """Lit un fichier du workspace"""
        try:
            full_path = WORKSPACE_DIR / filepath
            if not full_path.exists():
                return f"Fichier non trouvé: {filepath}"

            with open(full_path, 'r') as handle:
                return handle.read()
        except Exception as exc:
            return f"Erreur lecture: {exc}"

    def handle_message(self, message: str) -> str:
        """Traite un message de l'utilisateur"""

        intent = self.analyze_intent(message)

        if intent["needs_code_change"]:
            return self.execute_code_change(message)

        return self.chat_with_ollama(message)

    def git_command(self, args: List[str]) -> Dict[str, str]:
        """Exécute une commande git dans le workspace"""
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=WORKSPACE_DIR,
                capture_output=True,
                text=True
            )
            return {
                "code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except FileNotFoundError:
            return {"code": 1, "stdout": "", "stderr": "git non trouvé"}
        except Exception as exc:
            return {"code": 1, "stdout": "", "stderr": f"Erreur git: {exc}"}

    def review_changes(self) -> str:
        """Demande une revue de code sur le diff courant"""
        diff = self.git_command(["diff"])
        if diff["code"] != 0:
            return f"{Colors.FAIL}Erreur git diff: {diff['stderr']}{Colors.ENDC}"
        if not diff["stdout"]:
            return f"{Colors.WARNING}Aucun diff à revoir{Colors.ENDC}"

        status = self.git_command(["status", "-sb"])
        review_prompt = dedent(
            """
            You are a senior code reviewer. Review the following git diff for correctness,
            regressions, security issues, and missing tests. Answer concisely with bullet points,
            then provide a short action list.
            """
        ).strip()

        message = f"Git status:\n{status['stdout']}\n\nDiff:\n{diff['stdout']}"
        return self.chat_with_ollama(message, system_prompt=review_prompt)

    def commit_changes(self, commit_msg: str) -> str:
        """Effectue un commit sécurisé"""
        status = self.git_command(["status", "--porcelain"])
        if status["code"] != 0:
            return f"{Colors.FAIL}Erreur git status: {status['stderr']}{Colors.ENDC}"
        if not status["stdout"]:
            return f"{Colors.WARNING}Aucun changement à committer{Colors.ENDC}"

        if not self.ask_permission(f"Commiter les changements avec le message: {commit_msg}"):
            return f"{Colors.WARNING}Commit annulé{Colors.ENDC}"

        add_res = self.git_command(["add", "-A"])
        if add_res["code"] != 0:
            return f"{Colors.FAIL}Erreur git add: {add_res['stderr']}{Colors.ENDC}"

        commit_res = self.git_command(["commit", "-m", commit_msg])
        if commit_res["code"] != 0:
            err_msg = commit_res['stderr'] or commit_res['stdout']
            return f"{Colors.FAIL}Erreur git commit: {err_msg}{Colors.ENDC}"

        return f"{Colors.OKGREEN}✓ Commit créé:{Colors.ENDC}\n{commit_res['stdout']}"

    def set_stack(self, stack: str) -> str:
        """Active un preset de langage"""
        key = stack.lower()
        if key not in STACK_PRESETS:
            return f"{Colors.WARNING}Stacks disponibles: {', '.join(STACK_PRESETS.keys())}{Colors.ENDC}"

        preset = STACK_PRESETS[key]
        self.current_stack = key
        self.current_model = preset["model"]
        self.stack_prompt = preset["instructions"]
        return f"{Colors.OKGREEN}✓ Stack active: {key} (modèle: {self.current_model}){Colors.ENDC}"

    def handle_command(self, command: str) -> bool:
        """Gère les commandes spéciales"""

        if command in [":exit", ":quit", ":q"]:
            print(f"{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
            return False

        if command == ":help":
            self.print_banner()

        elif command == ":scan":
            self.scan_project()

        elif command == ":files":
            if not self.project_context.get("files"):
                self.scan_project()

            print(f"\n{Colors.BOLD}📁 Fichiers du workspace:{Colors.ENDC}\n")
            for f_name in sorted(self.project_context.get("files", [])):
                print(f"  {Colors.OKCYAN}•{Colors.ENDC} {f_name}")
            print()

        elif command == ":status":
            status = self.git_command(["status", "-sb"])
            if status["code"] == 0:
                print(f"{Colors.OKCYAN}{status['stdout'] or '(clean)'}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}Erreur git status: {status['stderr']}{Colors.ENDC}")

        elif command == ":review":
            print(f"{Colors.OKCYAN}🔍 Revue en cours...{Colors.ENDC}")
            review = self.review_changes()
            print(review)

        elif command.startswith(":commit"):
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                print(f"{Colors.WARNING}Usage: :commit \"message\"{Colors.ENDC}")
            else:
                result = self.commit_changes(parts[1])
                print(result)

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
                status_flag = "activé" if self.auto_approve else "désactivé"
                print(f"Auto-approve: {status_flag}")

        elif command.startswith(":model"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                self.current_model = parts[1]
                print(f"{Colors.OKGREEN}✓ Modèle: {self.current_model}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}Usage: :model <nom>{Colors.ENDC}")

        elif command.startswith(":stack"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                feedback = self.set_stack(parts[1])
                print(feedback)
            else:
                print(f"{Colors.WARNING}Usage: :stack <php|unity|js|react|bash|python>{Colors.ENDC}")

        elif command == ":clear":
            self.conversation_history = []
            self.project_context = {}
            self.current_stack = None
            self.stack_prompt = None
            print(f"{Colors.OKGREEN}✓ Contexte effacé{Colors.ENDC}")

        else:
            print(f"{Colors.FAIL}❌ Commande inconnue: {command}{Colors.ENDC}")
            print(f"{Colors.WARNING}Tapez :help pour l'aide{Colors.ENDC}")

        return True

    def run(self):
        """Boucle principale"""
        self.print_banner()

        if not self.check_ollama():
            return

        print(f"{Colors.OKGREEN}✓ Connecté à Ollama{Colors.ENDC}\n")

        self.scan_project()
        print()

        try:
            while True:
                auto_status = f"{Colors.DIM}[auto]{Colors.ENDC} " if self.auto_approve else ""
                prompt = f"{auto_status}{Colors.BOLD}You>{Colors.ENDC} "

                try:
                    user_input = input(prompt).strip()
                except EOFError:
                    print()
                    break

                if not user_input:
                    continue

                if user_input.startswith(":"):
                    if not self.handle_command(user_input):
                        break
                    continue

                print(f"\n{Colors.OKCYAN}🤖 Claudine réfléchit...{Colors.ENDC}\n")

                response = self.handle_message(user_input)

                print(f"{Colors.OKGREEN}{Colors.BOLD}Claudine>{Colors.ENDC}")
                print(response)
                print()

                self.conversation_history.append({
                    "user": user_input,
                    "assistant": response
                })

        except KeyboardInterrupt:
            print(f"\n\n{Colors.OKGREEN}👋 Au revoir !{Colors.ENDC}")
        finally:
            try:
                readline.write_history_file(HISTORY_FILE)
            except Exception:
                pass
            self.client.close()


def main():
    agent = SmartAgent()
    agent.run()


if __name__ == "__main__":
    main()
