# Anime Cleaner 🎬

A simple automation that cleans up anime video files by:  

- Keeping only **English & Japanese audio** (default = English).  
- Keeping only **English, Japanese, and Hebrew subtitles**.  
- Skipping files that are already correctly configured.  
- Sending a **daily summary to Telegram**.  

Runs automatically once a day at **midnight** inside Docker.  

---

## 📦 Requirements

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  
- A working [Telegram bot token](https://core.telegram.org/bots#botfather) and chat ID  

---

## ⚙️ Setup

Clone the repo and enter the folder:

```bash
git clone <your-repo-url>
cd anime_fixer
```

Create your `.env` from the template:

```bash
cp .env.example .env
```

Fill in your values:

```env
ANIME_LIBRARY_PATH=/mnt/media/anime
MAX_WORKERS=4

TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

ALLOWED_SUBS=eng,jpn,heb
ALLOWED_AUDIO=eng,jpn
```

Build and start the container:

```bash
docker compose up -d --build
```

---

## 🔄 How it works

- When the container starts, it runs immediately.  
- Then it runs every day at **midnight**.  
- For each file in your anime library:  
  - ✅ Processed if not compliant  
  - ⏩ Skipped if already fixed  
  - ❌ Logged as failed if an error occurred  
- A **summary is sent to Telegram** after each run.  

---

## 📝 Logs

Follow the container logs live:

```bash
docker logs -f anime-fixer
```

---

## 🛑 Stop / Remove

Stop the service:

```bash
docker compose down
```

Remove everything (including the image):

```bash
docker compose down --rmi all
```

---

## 📊 Example Telegram Summary

```
Anime fixer summary
Total: 120
Processed: 12
Skipped: 106
Failed: 2
```