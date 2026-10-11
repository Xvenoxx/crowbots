# CrowBots

CrowBots est un bot Discord de modération léger et facile à personnaliser. Il inclut des commandes de base comme bannir, expulser, supprimer des messages, muter et démuter.

## Fonctionnalités

- +help : affiche les commandes disponibles
- +ban : bannir un membre
- +kick : expulser un membre
- +clear : supprimer des messages
- +mute : mettre en sourdine un membre temporairement
- +unmute : retirer le mute
- Gestion des erreurs utilisateur

## Prérequis

- Python 3.10+
- Un bot Discord avec le token de l'application
- Les permissions nécessaires sur le serveur

## Installation

1. Clone le projet
   ```bash
   git clone https://github.com/Xvenoxx/crowbots.git
   cd crowbots
   ```

2. Crée un environnement virtuel
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. Installe les dépendances
   ```bash
   pip install -r requirements.txt
   ```

4. Configure le token
   ```bash
   cp .env.example .env
   ```

5. Modifie `.env` avec ton token Discord
   ```env
   DISCORD_TOKEN=ton_token_ici
   ```

6. Lancer le bot
   ```bash
   python main.py
   ```

## Commandes

- `+help`
- `+ban @membre [raison]`
- `+kick @membre [raison]`
- `+clear nombre`
- `+mute @membre [minutes] [raison]`
- `+unmute @membre`

## Sécurité

Le bot vérifie les permissions avant chaque action de modération. Si une permission manque, il répond avec un message clair.

## Licence

MIT
