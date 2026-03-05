# Configuration Client/Serveur Claudine

Guide pour utiliser Claudine en mode **client/serveur** : votre PC puissant héberge les modèles AI, votre Mac/laptop léger se connecte à distance.

## 📐 Architecture

```
┌─────────────────────────────────────────────────┐
│  CLIENT (Mac Bureau / Laptop)                   │
│                                                 │
│  • Agents CLI Python uniquement                 │
│  • Aucun Docker local requis                    │
│  • ~100 MB d'espace disque                      │
│  • Connexion via tunnel SSH sécurisé            │
│                                                 │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Tunnel SSH
                   │ ou VPN
                   │
┌──────────────────▼───────────────────────────────┐
│  SERVEUR (PC Puissant / Maison)                  │
│                                                  │
│  • Docker avec Ollama + Modèles                  │
│  • 32-64 GB RAM pour gros modèles                │
│  • API Claudine FastAPI                          │
│  • Optionnel : GPU NVIDIA                        │
│                                                  │
└──────────────────────────────────────────────────┘
```

## 🎯 Cas d'Usage

✅ **Idéal pour** :
- PC puissant à la maison, laptop léger au bureau
- Serveur dédié avec GPU, accès depuis plusieurs machines
- Partage de modèles AI lourds entre plusieurs développeurs
- Éviter de télécharger 20 GB de modèles sur chaque machine

❌ **Pas adapté si** :
- Vous n'avez qu'une seule machine
- Connexion internet instable
- Latence critique (préférez installation locale)

---

## 🖥️  PARTIE 1 : Configuration Serveur

### Prérequis Serveur

- Linux, macOS ou Windows avec WSL
- Docker & Docker Compose
- 32-64 GB RAM (pour modèles 32B+)
- 50+ GB espace disque
- Optionnel : GPU NVIDIA avec CUDA

### Installation Serveur

```bash
# 1. Cloner le repository
git clone https://github.com/kmoussouni/ai-claudine-code.git
cd ai-claudine-code

# 2. Configurer pour mode serveur
# IMPORTANT : Utilisez .env.server comme base pour le serveur
cp .env.server .env

# 3. Éditer .env pour personnaliser
nano .env
```

**⚠️  Important** : Le fichier `.env.server` contient la configuration optimale pour un serveur puissant (modèle 32b par défaut, sécurité renforcée). Ne pas utiliser le `.env.example` qui est pour usage local avec modèles légers.

**Configuration .env importante** :

```bash
# Gros modèles (vous avez la RAM !)
DEFAULT_MODEL=qwen2.5-coder:32b

# Générer un token sécurisé
# openssl rand -hex 32
CLAUDINE_API_TOKEN=votre_token_securise_ici

# Accepter connexions externes
API_HOST=0.0.0.0

# GPU si disponible (décommentez dans docker-compose.yml aussi)
# NVIDIA_VISIBLE_DEVICES=all
```

### Démarrer le Serveur

```bash
# Installation et démarrage
./scripts/setup.sh

# Vérifier que tout fonctionne
make status

# Voir les logs
docker-compose logs -f
```

### Exposer le Serveur

#### Option A : Tunnel SSH (Recommandé)

**Avantages** : Sécurisé, pas besoin d'IP publique, firewall friendly

Aucune configuration supplémentaire sur le serveur !

#### Option B : VPN (Tailscale, WireGuard)

**Avantages** : Connexion toujours active, plusieurs clients faciles

```bash
# Installer Tailscale (exemple)
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Noter l'IP Tailscale
tailscale ip
```

#### Option C : IP Publique + Firewall

**Avantages** : Performance max, pas de tunnel

**⚠️  Attention** : Nécessite configuration firewall et HTTPS

```bash
# Ouvrir les ports (exemple avec ufw)
sudo ufw allow 3000/tcp comment 'Claudine API'
sudo ufw allow 11434/tcp comment 'Ollama'

# Configurer un reverse proxy nginx avec SSL
# Voir docs/nginx-reverse-proxy.md
```

### Sécurité Serveur

```bash
# 1. Firewall : N'exposez QUE ce qui est nécessaire
sudo ufw status

# 2. Token API : TOUJOURS utiliser un token fort
grep CLAUDINE_API_TOKEN .env

# 3. HTTPS : Si exposition publique, utilisez SSL
# Exemple avec Let's Encrypt + nginx

# 4. Logs : Surveillez les accès
docker-compose logs -f | grep "POST /chat"

# 5. Mises à jour : Gardez Docker et Ollama à jour
docker-compose pull
```

---

## 💻 PARTIE 2 : Configuration Client

### Prérequis Client

- Python 3.8+
- SSH configuré (si tunnel SSH)
- ~100 MB d'espace disque

### Installation Client Léger

#### Option A : Clone Complet (Recommandé)

```bash
# Clone le repo (pour avoir les scripts)
git clone https://github.com/kmoussouni/ai-claudine-code.git claudine-client
cd claudine-client

# Installation client (automatique via make)
make client-install

# Ou manuellement
./scripts/install-client.sh
```

Cette commande installe automatiquement toutes les dépendances Python depuis `requirements-cli.txt` :
- `httpx` - Client HTTP pour communiquer avec le serveur
- `textual` - Interface TUI pour l'agent interactif
- `rich` - Affichage amélioré dans le terminal
- `pygments` - Coloration syntaxique

#### Option B : Installation Minimale

```bash
# Créer un dossier
mkdir claudine-client && cd claudine-client

# Télécharger seulement les scripts nécessaires
curl -O https://raw.githubusercontent.com/kmoussouni/ai-claudine-code/main/scripts/claudine-smart.py
curl -O https://raw.githubusercontent.com/kmoussouni/ai-claudine-code/main/scripts/agent-interactive.py
curl -O https://raw.githubusercontent.com/kmoussouni/ai-claudine-code/main/scripts/connect-remote.sh
curl -O https://raw.githubusercontent.com/kmoussouni/ai-claudine-code/main/requirements-cli.txt

chmod +x *.py connect-remote.sh

# Installer dépendances depuis requirements-cli.txt
pip3 install --user -r requirements-cli.txt

# Ou installation manuelle minimale
# pip3 install --user httpx
```

### Configuration Client

```bash
# Copier la config client
cp .env.client .env

# Éditer .env
nano .env
```

**Configuration .env client** :

```bash
# URLs (via tunnel SSH)
CLAUDINE_API_URL=http://localhost:3000
OLLAMA_API_BASE=http://localhost:11434

# OU via VPN (exemple Tailscale)
# CLAUDINE_API_URL=http://100.64.1.2:3000
# OLLAMA_API_BASE=http://100.64.1.2:11434

# Token (même que sur le serveur)
CLAUDINE_API_TOKEN=votre_token_securise_ici

# Modèle (doit être installé sur le serveur)
DEFAULT_MODEL=qwen2.5-coder:32b

# Serveur distant (pour script connect-remote.sh)
CLAUDINE_REMOTE_HOST=monserveur.com
CLAUDINE_REMOTE_USER=karim
```

---

## 🔐 PARTIE 3 : Connexion Client → Serveur

### Méthode 1 : Tunnel SSH (Recommandé)

#### Configuration SSH

Sur le **client**, assurez-vous que vous pouvez SSH vers le serveur :

```bash
# Tester la connexion SSH
ssh utilisateur@monserveur.com

# Si première fois, copier votre clé publique
ssh-copy-id utilisateur@monserveur.com
```

#### Démarrer le Tunnel

```bash
# Méthode simple
./scripts/connect-remote.sh start --host monserveur.com

# Avec options
./scripts/connect-remote.sh start \
  --host monserveur.com \
  --user karim \
  --key ~/.ssh/id_rsa

# Ou via variable d'environnement
export CLAUDINE_REMOTE_HOST=monserveur.com
./scripts/connect-remote.sh start
```

Le tunnel crée automatiquement :
- `localhost:3000` → API Claudine
- `localhost:11434` → Ollama
- `localhost:8080` → Web UI

#### Vérifier le Tunnel

```bash
# Status du tunnel
./scripts/connect-remote.sh status

# Tester l'API
curl http://localhost:3000/health
```

#### Utiliser les Agents

Une fois le tunnel actif :

```bash
# Agent Smart (recommandé)
python3 scripts/claudine-smart.py

# Agent Interactif
python3 scripts/agent-interactive.py

# Agent TUI
python3 scripts/agent-tui.py

# Web UI dans le navigateur
open http://localhost:8080
```

#### Arrêter le Tunnel

```bash
./scripts/connect-remote.sh stop
```

### Méthode 2 : VPN (Tailscale)

#### Sur le Serveur

```bash
# Installer Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Noter l'IP
tailscale ip
# Exemple : 100.64.1.2
```

#### Sur le Client

```bash
# Installer Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Dans .env
CLAUDINE_API_URL=http://100.64.1.2:3000
OLLAMA_API_BASE=http://100.64.1.2:11434
```

Pas besoin de tunnel ! Connexion directe.

```bash
# Utiliser directement les agents
python3 scripts/claudine-smart.py
```

### Méthode 3 : IP Publique + HTTPS

#### Sur le Serveur (avec nginx)

```bash
# Installer nginx et certbot
sudo apt install nginx certbot python3-certbot-nginx

# Configurer nginx (exemple)
sudo nano /etc/nginx/sites-available/claudine
```

```nginx
server {
    listen 443 ssl;
    server_name claudine.votredomaine.com;

    ssl_certificate /etc/letsencrypt/live/claudine.votredomaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/claudine.votredomaine.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Activer et obtenir certificat SSL
sudo ln -s /etc/nginx/sites-available/claudine /etc/nginx/sites-enabled/
sudo certbot --nginx -d claudine.votredomaine.com
sudo systemctl restart nginx
```

#### Sur le Client

```bash
# Dans .env
CLAUDINE_API_URL=https://claudine.votredomaine.com
```

---

## 💡 Workflows Recommandés

### Workflow Bureau → Maison

```bash
# Le matin au bureau
cd ~/claudine-client
./scripts/connect-remote.sh start --host maison.local
python3 scripts/claudine-smart.py

# Travailler normalement...

# Le soir avant de partir
./scripts/connect-remote.sh stop
```

### Workflow Permanent (VPN)

```bash
# Une seule fois : configurer Tailscale
# Puis utiliser directement sans tunnel

python3 scripts/claudine-smart.py
```

### Workflow Multi-Machines

```bash
# Serveur : PC Windows avec GPU RTX 4090
# Client 1 : Mac Bureau
# Client 2 : Laptop Linux déplacement
# Client 3 : iPad avec SSH client

# Tous connectent au même serveur via VPN
# Partagent les mêmes modèles 70B
```

---

## 🐛 Dépannage

### "ModuleNotFoundError: No module named 'httpx'"

**Problème** : Les dépendances Python du client ne sont pas installées.

**Solution** :
```bash
# Sur votre machine cliente
cd claudine-client

# Option 1 : Via make (recommandé)
make client-install

# Option 2 : Via script
./scripts/install-client.sh

# Option 3 : Installation manuelle
pip3 install --user -r requirements-cli.txt
```

### Le serveur utilise le mauvais modèle (7b au lieu de 32b)

**Problème** : Le fichier `.env` sur le serveur n'a pas été correctement configuré.

**Solution sur le serveur** :
```bash
# Vérifier la configuration actuelle
cat .env | grep DEFAULT_MODEL

# Si c'est qwen2.5-coder:7b, corriger :
cp .env.server .env
# Ou éditer directement :
nano .env  # Changer DEFAULT_MODEL=qwen2.5-coder:32b

# Redémarrer les services
make restart

# Vérifier que le modèle est installé
docker-compose exec ollama ollama list
```

### "Connection refused"

```bash
# Vérifier que le tunnel est actif
./scripts/connect-remote.sh status

# Vérifier que le serveur écoute
# Sur le serveur :
docker-compose ps
curl http://localhost:3000/health

# Tester SSH
ssh -v utilisateur@serveur.com
```

### Tunnel SSH se Déconnecte

```bash
# Le script gère automatiquement les keepalive
# Mais vous pouvez ajouter dans ~/.ssh/config :

Host monserveur
    HostName monserveur.com
    User karim
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Performance Lente

- Vérifiez votre ping : `ping monserveur.com`
- Latence <50ms : Excellent
- Latence 50-150ms : Correct
- Latence >200ms : Peut être lent pour usage interactif

Solution : Utilisez un serveur plus proche ou un VPN optimisé

### Modèle Non Trouvé

```bash
# Sur le serveur, vérifier les modèles installés
docker-compose exec ollama ollama list

# Installer le modèle manquant
docker-compose exec ollama ollama pull qwen2.5-coder:32b
```

---

## 📊 Comparaison Méthodes de Connexion

| Méthode | Sécurité | Setup | Performance | Coût |
|---------|----------|-------|-------------|------|
| Tunnel SSH | 🟢🟢🟢 | 🟢 Facile | 🟡 Bonne | 🟢 Gratuit |
| VPN (Tailscale) | 🟢🟢🟢 | 🟢 Facile | 🟢 Excellente | 🟢 Gratuit |
| IP Publique | 🟡 Moyenne | 🔴 Complexe | 🟢🟢 Meilleure | 🟡 Variable |

**Recommandation** :
- **Tunnel SSH** : Simple, sécurisé, parfait pour commencer
- **VPN** : Meilleur si connexions fréquentes
- **IP Publique** : Performance max mais complexe

---

## 🚀 Avantages du Mode Client/Serveur

✅ **Économie** :
- Un seul serveur puissant au lieu de plusieurs
- Pas besoin de télécharger les modèles sur chaque machine
- Partagez le GPU entre plusieurs utilisateurs

✅ **Flexibilité** :
- Travaillez depuis n'importe quelle machine
- Laptop léger avec puissance d'un serveur
- Même configuration partout

✅ **Gestion** :
- Un seul point de mise à jour
- Modèles centralisés
- Logs centralisés

✅ **Performance** :
- Utilisez de très gros modèles (70B+)
- GPU dédié au serveur
- Le client reste léger et rapide

---

## 📚 Voir Aussi

- [README.md](README.md) - Documentation principale
- [AGENT-SMART.md](AGENT-SMART.md) - Agent Smart guide
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide local

---

**Vous êtes maintenant prêt à utiliser Claudine en mode client/serveur ! 🎉**
