# Manuel - A Discord Basic Bot 🤖

**Manuel** is a Discord bot built with [discord.py](https://discordpy.readthedocs.io/), designed to enhance community management with utility commands, customizable welcome messages, and event logging.

> “Easy there, Manuel’s still alive...”  
> — you, after a `/song_request`

---
## Features

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

- `on_member_join` – 
  - Logs whenever a new member joins the server.

### 🎵 Music Commands
- `/play [query_or_link]` — Plays a YouTube link or searches and plays a song.
- `/pause` — Pauses the current track.
- `/resume` — Resumes playback.
- `/skip` — Skips the current track.
- `/stop` — Stops playback and clears the queue.
- **Queue per server** (`guild_id`)
- **Checks if user is in a voice channel**
- **Simple feedback via interaction messages**

### 🛡️ Admin Tools
- `/shutdown` – Shuts down the bot. Only available to authorized users.
- `/kick` – Kicks a member from the server.
- `/ban` – Bans a member from the server.
- `/mute` – Mutes a member by assigning a mute role (you must configure a "Muted" role).
- `/unmute` – Unmutes a previously muted member.
- `/purge` – Deletes a specified number of messages from a channel (bulk delete).


### 🔧 Server Info & Config

- `/userinfo` – Displays detailed information about a server member.
- `/serverinfo` – Shows general information about the current server.
- `/say` – The bot repeats the provided message.
- `/preview_welcome` – Shows a preview of the currently configured welcome message.
- `/set_welcome_channel` – Sets the channel where welcome messages are sent.
- `/set_welcome_message` – Sets the welcome message content. Supports placeholders like `{user}` and `{server}`.
- `/toggle_welcome` – Enables or disables welcome messages.


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

## 👤 Author
Created by Thiago Correali <br>
Bot logic and architecture built with modular design and future extensibility in mind.

## 📝 License
MIT License