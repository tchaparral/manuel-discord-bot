# Manuel - A Discord Basic Bot (MVP)

Manuel is a modular Discord bot focused on music playback via YouTube links or search queries. Built with `discord.py` using modern Slash Commands (`app_commands`), it provides basic song request functionality in voice channels, with per-server queues and admin permission handling.

---

##  Current Features (Sprint 1)

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
discord_bot/
│
├── cogs/
│ ├── music.py # All music-related slash commands
│ └── admin_tools.py # Shutdown and admin-only logic
│
├── utils/
│ ├── yt_downloader.py # YouTube audio download logic
│ └── utils.py # Shared helpers
│
├── data/ # Runtime cache and logs (ignored by Git)
│
├── temp/song_request/ # Temporary song files (ignored by Git)
│
├── manuel.py # Bot entrypoint
├── config.py # Configuration loader (token, secrets)
├── test.py # Dev test runner
├── requirements.txt # Dependencies
└── .env # Environment variables (not committed)
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

Roles system

XP system

Sky is limit...

## 👤 Author
Created by Thiago Correali <br>
Bot logic and architecture built with modular design and future extensibility in mind.

## 📝 License
MIT License