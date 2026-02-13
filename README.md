# 💖 Telegram Love Game Engine

A cinematic, multi-session Telegram group love game platform built with Pyrogram (Python 3.11+).

Real proposals. Anonymous crushes. Savage pranks. Dramatic breakups.  
Premium Telegram group experience.

---

## 🚀 Deploy to Heroku (One-Click)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Oxeigns/Valentine)

> ⚠️ Make sure your repository contains:
> - app.json  
> - Procfile  
> - requirements.txt  
> - runtime.txt  

Otherwise the deploy button will fail.

---

## ✨ Features

- 💘 Real Proposal Mode
- 💌 Anonymous Crush Mode
- 🎭 Fake Proposal Prank Mode
- 💔 Breakup Drama Mode
- 🏆 Leaderboard System
- Multi-session support (multiple love stories in same group)
- 5-minute session expiry
- 20-second per-mode cooldown
- Anti-spam protection
- Persistent JSON storage
- Heroku Ready
- Fully Async Architecture

---

## 📜 Commands

/love        - Open main menu  
/propose     - Real proposal (reply required)  
/crush       - Anonymous crush (reply required)  
/prank       - Fake proposal prank (reply required)  
/breakup     - End your love story  
/loveboard   - View rankings  
/help        - Help menu
/vibe        - Random Valentine vibe drop  

---

## ⚙️ Required Environment Variables

| Variable   | Description |
|------------|------------|
| API_ID     | Get from https://my.telegram.org |
| API_HASH   | Get from https://my.telegram.org |
| BOT_TOKEN  | Get from @BotFather |

---

## 🛠 Manual Deployment (Heroku CLI)

Clone repository:

git clone https://github.com/Oxeigns/Valentine.git  
cd Valentine  

Create Heroku app:

heroku create your-app-name  

Set config variables:

heroku config:set API_ID=xxxx  
heroku config:set API_HASH=xxxx  
heroku config:set BOT_TOKEN=xxxx  

Deploy:

git push heroku main  

Scale worker dyno:

heroku ps:scale worker=1  

---

## 🖥 Local Testing

Install dependencies:

pip install -r requirements.txt  

Set environment variables:

Linux/macOS:
export API_ID=xxxx  
export API_HASH=xxxx  
export BOT_TOKEN=xxxx  

Windows:
set API_ID=xxxx  
set API_HASH=xxxx  
set BOT_TOKEN=xxxx  

Run:

python main.py  

---

## 🔒 Production Notes

- Use worker dyno (NOT web).
- Do NOT bind to PORT.
- Sessions expire automatically after 5 minutes.
- Max 10 active sessions per group.
- Max 3 active sessions per user.
- All data stored in:
  - couples.json
  - leaderboard.json

---

## 🧠 Architecture Overview

- Async Pyrogram Client
- Multi-session state manager
- JSON persistent storage
- Inline button-driven UX
- Central callback router
- Modular engine design

---

## 👑 Built For

Telegram groups that want:

Drama.  
Fun.  
Competition.  
Savage energy.  
Premium interaction.  

---

Made with ❤️ using Pyrogram.
