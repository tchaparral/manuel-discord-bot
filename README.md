# Manuel - A Discord Basic Bot (MVP)

**Manuel** is a custom Discord bot designed for lightweight moderation, text-based interactions, and eventually music control. It now features a structured permissions system and full logging, aiming to grow into a modular assistant for community servers.

> “Easy there, Manuel’s still alive...”  
> — you, after a `/song_request`

---
## Features Implemented in This Sprint

### 🔐 Custom Role-Based Permission System
You can now assign specific server roles as `admin` or `user`, stored persistently using **SQLite**:

- `/set_admin <role>`: define a role as admin.
- `/set_user <role>`: define a role as user.
- Permission levels are enforced using decorators: `@is_owner`, `@is_admin`, and `@is_user`.
- Only one role per type (admin/user) is active per guild.
- Built-in **autocomplete** for role names in slash commands.


### 📝 Structured Logging System
Every command and error is logged in real time, following a clean format:

```text
2025-05-15 11:03:04,123 - __main__ - INFO - {message}
2025-05-15 11:03:04,456 - __main__ - ERROR - {error}
```

##  Previous Features

### 🎵 Music Commands
- `/play [query_or_link]` — Plays a YouTube link or searches and plays a song.
- `/pause` — Pauses the current track.
- `/resume` — Resumes playback.
- `/skip` — Skips the current track.
- `/stop` — Stops playback and clears the queue.
- **Queue per server** (`guild_id`)
- **Checks if user is in a voice channel**
- **Simple feedback via interaction messages**

### 👑 Admin Commands
- `/shutdown` — Shuts down the bot (owner-only).
- Console logging for basic actions.
- Owner-only decorator check.

## 🗂️ Project Structure
```
├── assets/ # Static assets (empty or not shown)
├── cogs/ # Bot command modules
│ ├── admin_tools.py
│ ├── music.py
│ └── role_manager.py
├── data/ # Placeholder or future data storage
├── db/ # SQLite database and DB logic
│ ├── manuel_roles.db
│ └── role_db.py
├── logs/ # Log output folder
├── temp/ # Temporary data
├── utils/ # Utility modules
│ ├── permissions.py
│ ├── utils.py
│ └── yt_downloader.py
├── venv/ # Virtual environment (excluded via .gitignore)
├── .env # Environment variables
├── .gitignore
├── config.py # Configuration logic
├── license.txt
├── logging_config.py # Logging setup (file handlers, formats)
├── manuel.py # Main bot entrypoint
├── README.md
└── requirements.txt
```

## 📦 Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/manuel-discord-bot.git
cd manuel-discord-bot
```
2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a .env file with your bot token:
```bash
DISCORD_TOKEN=your_bot_token_here
```
5. Run the bot:
```
python manuel.py
```

## 🧭 Roadmap (Future Sprints)
/queue — View the current queue

/nowplaying — Display currently playing song

/remove — Remove a song from the queue

Auto-disconnect if voice channel is empty

Persistent queue between restarts

Spotify search and integration

Web dashboard for managing songs and analytics

XP system

Sky is limit...

## 👤 Author
Created by Thiago Correali <br>
Bot logic and architecture built with modular design and future extensibility in mind.

## 📝 License
MIT License