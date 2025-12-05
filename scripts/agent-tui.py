#!/usr/bin/env python3
"""
Claudine TUI Agent
Interface Terminal avancée avec vue splitée
Nécessite: pip install textual httpx
"""

import os
import asyncio
from pathlib import Path
from typing import List
import httpx

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
    from textual.widgets import Header, Footer, Static, Input, Button, TextLog, Label
    from textual.binding import Binding
    from textual import events
    from textual.reactive import reactive
except ImportError:
    print("❌ Textual n'est pas installé")
    print("   Installez avec: pip3 install textual")
    exit(1)

# Configuration
API_BASE_URL = os.getenv("CLAUDINE_API_URL", "http://localhost:3000")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5-coder:7b")

class ChatMessage(Static):
    """Widget pour un message de chat"""

    def __init__(self, sender: str, message: str, **kwargs):
        super().__init__(**kwargs)
        self.sender = sender
        self.message = message

    def compose(self) -> ComposeResult:
        if self.sender == "user":
            yield Label(f"[bold cyan]You:[/bold cyan] {self.message}")
        else:
            yield Label(f"[bold green]Agent:[/bold green] {self.message}")


class FilesList(Static):
    """Widget pour afficher les fichiers en contexte"""

    files = reactive([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files = []

    def render(self) -> str:
        if not self.files:
            return "[dim]Aucun fichier en contexte[/dim]"
        return "\n".join([f"[cyan]•[/cyan] {f}" for f in self.files])


class StatusBar(Static):
    """Barre de statut"""

    status = reactive("Prêt")
    model = reactive(DEFAULT_MODEL)

    def render(self) -> str:
        return f"[bold]Status:[/bold] {self.status} | [bold]Modèle:[/bold] {self.model}"


class ClaudineTUI(App):
    """Application TUI principale"""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 3;
        grid-rows: 1fr 3fr auto;
        grid-columns: 3fr 1fr;
    }

    #header {
        column-span: 2;
        height: 3;
        background: $boost;
        content-align: center middle;
        text-style: bold;
    }

    #chat-container {
        row-span: 1;
        border: solid $primary;
        height: 100%;
    }

    #sidebar {
        row-span: 1;
        border: solid $secondary;
        padding: 1;
    }

    #input-container {
        column-span: 2;
        height: auto;
        background: $surface;
        padding: 1;
        layout: horizontal;
    }

    #message-input {
        width: 4fr;
    }

    #send-button {
        width: 1fr;
        margin-left: 1;
    }

    TextLog {
        height: 100%;
        scrollbar-gutter: stable;
    }

    .chat-message {
        margin: 1;
        padding: 1;
    }

    #status-bar {
        column-span: 2;
        height: 1;
        background: $panel;
        padding: 0 1;
    }

    #files-list {
        margin-top: 1;
        padding: 1;
        border: solid $accent;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quitter"),
        Binding("ctrl+l", "clear", "Effacer"),
        Binding("ctrl+f", "toggle_files", "Fichiers"),
    ]

    def __init__(self):
        super().__init__()
        self.client = httpx.AsyncClient(timeout=300.0)
        self.current_files: List[str] = []
        self.current_model = DEFAULT_MODEL

    def compose(self) -> ComposeResult:
        """Créer l'interface"""
        yield Header()

        # Zone de chat
        with Container(id="chat-container"):
            yield TextLog(id="chat-log", highlight=True, markup=True)

        # Sidebar
        with Vertical(id="sidebar"):
            yield Label("[bold]📁 Fichiers en contexte[/bold]")
            yield FilesList(id="files-list")
            yield Label("\n[bold]💡 Raccourcis[/bold]")
            yield Label("[dim]Ctrl+C[/dim] Quitter")
            yield Label("[dim]Ctrl+L[/dim] Effacer")
            yield Label("\n[bold]📝 Commandes[/bold]")
            yield Label("[dim]:files[/dim] Gérer fichiers")
            yield Label("[dim]:model[/dim] Changer modèle")
            yield Label("[dim]:help[/dim] Aide")

        # Zone d'input
        with Horizontal(id="input-container"):
            yield Input(placeholder="Votre message...", id="message-input")
            yield Button("Envoyer", variant="primary", id="send-button")

        # Barre de statut
        yield StatusBar(id="status-bar")

        yield Footer()

    async def on_mount(self) -> None:
        """Appelé au démarrage"""
        chat_log = self.query_one("#chat-log", TextLog)
        status_bar = self.query_one("#status-bar", StatusBar)

        chat_log.write("[bold cyan]╔══════════════════════════════════════════════════════════╗[/bold cyan]")
        chat_log.write("[bold cyan]║          Claudine - Agent TUI Interactif                ║[/bold cyan]")
        chat_log.write("[bold cyan]╚══════════════════════════════════════════════════════════╝[/bold cyan]")
        chat_log.write("")

        # Vérifier la connexion
        try:
            response = await self.client.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                chat_log.write("[green]✓ Connecté au serveur Claudine[/green]")
                status_bar.status = "[green]Connecté[/green]"
            else:
                chat_log.write("[red]❌ Erreur de connexion[/red]")
                status_bar.status = "[red]Déconnecté[/red]"
        except Exception as e:
            chat_log.write(f"[red]❌ Erreur: {e}[/red]")
            chat_log.write("[yellow]Assurez-vous que les services sont démarrés: make start[/yellow]")
            status_bar.status = "[red]Erreur[/red]"

        chat_log.write("")
        chat_log.write("[dim]Tapez votre message et appuyez sur Entrée ou cliquez Envoyer[/dim]")
        chat_log.write("")

        # Focus sur l'input
        self.query_one("#message-input").focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Gère le clic sur le bouton Envoyer"""
        if event.button.id == "send-button":
            await self.send_message()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Gère l'appui sur Entrée dans l'input"""
        if event.input.id == "message-input":
            await self.send_message()

    async def send_message(self) -> None:
        """Envoie un message à l'agent"""
        message_input = self.query_one("#message-input", Input)
        chat_log = self.query_one("#chat-log", TextLog)
        status_bar = self.query_one("#status-bar", StatusBar)

        message = message_input.value.strip()
        if not message:
            return

        # Effacer l'input
        message_input.value = ""

        # Afficher le message de l'utilisateur
        chat_log.write(f"[bold cyan]You:[/bold cyan] {message}")

        # Commande spéciale
        if message.startswith(":"):
            self.handle_command(message)
            return

        # Envoyer à l'API
        status_bar.status = "[yellow]Agent réfléchit...[/yellow]"

        try:
            response = await self.client.post(
                f"{API_BASE_URL}/chat",
                json={
                    "message": message,
                    "files": self.current_files,
                    "model": self.current_model
                }
            )

            if response.status_code == 200:
                data = response.json()
                agent_response = data["response"]

                # Afficher la réponse
                chat_log.write(f"[bold green]Agent:[/bold green]")
                chat_log.write(agent_response)
                chat_log.write("")

                status_bar.status = "[green]Prêt[/green]"
            else:
                chat_log.write(f"[red]❌ Erreur {response.status_code}[/red]")
                status_bar.status = "[red]Erreur[/red]"

        except httpx.TimeoutException:
            chat_log.write("[red]⏱️  Timeout: l'opération a pris trop de temps[/red]")
            status_bar.status = "[red]Timeout[/red]"
        except Exception as e:
            chat_log.write(f"[red]❌ Erreur: {e}[/red]")
            status_bar.status = "[red]Erreur[/red]"

    def handle_command(self, command: str) -> None:
        """Gère les commandes spéciales"""
        chat_log = self.query_one("#chat-log", TextLog)
        files_list = self.query_one("#files-list", FilesList)
        status_bar = self.query_one("#status-bar", StatusBar)

        if command == ":help":
            chat_log.write("[bold]Commandes disponibles:[/bold]")
            chat_log.write("  :files [file1 file2 ...] - Définir les fichiers de contexte")
            chat_log.write("  :model <nom>             - Changer de modèle")
            chat_log.write("  :clear                   - Effacer l'historique")
            chat_log.write("  :help                    - Afficher cette aide")
            chat_log.write("")

        elif command.startswith(":files"):
            parts = command.split()[1:]
            if parts:
                self.current_files = parts
                files_list.files = parts
                chat_log.write(f"[green]✓ Fichiers définis: {', '.join(parts)}[/green]")
            else:
                self.current_files = []
                files_list.files = []
                chat_log.write("[yellow]Contexte de fichiers effacé[/yellow]")
            chat_log.write("")

        elif command.startswith(":model"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                self.current_model = parts[1]
                status_bar.model = parts[1]
                chat_log.write(f"[green]✓ Modèle changé: {self.current_model}[/green]")
            else:
                chat_log.write("[yellow]Usage: :model <nom-du-modele>[/yellow]")
            chat_log.write("")

        elif command == ":clear":
            chat_log.clear()
            chat_log.write("[green]✓ Historique effacé[/green]")
            chat_log.write("")

        else:
            chat_log.write(f"[red]❌ Commande inconnue: {command}[/red]")
            chat_log.write("[dim]Tapez :help pour voir les commandes disponibles[/dim]")
            chat_log.write("")

    def action_clear(self) -> None:
        """Action pour Ctrl+L"""
        chat_log = self.query_one("#chat-log", TextLog)
        chat_log.clear()
        chat_log.write("[green]✓ Historique effacé[/green]")
        chat_log.write("")

    async def on_unmount(self) -> None:
        """Nettoyage à la fermeture"""
        await self.client.aclose()


def main():
    try:
        app = ClaudineTUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")

if __name__ == "__main__":
    main()
