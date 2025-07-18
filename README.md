# 🤖 TrafficBot - Telegram Bot for Monitoring Marzneshin Traffic

**TrafficBot** is a personal Telegram bot that fetches user traffic statistics from the **Marzneshin panel** via its API and displays it interactively through Telegram.

---

## 🚀 Features

- Login with username and password (SUDO admin only)
- Fetch traffic usage from Marzneshin API
- Supports multiple time ranges: 24h, 7d, 30d, 3m
- Clean and interactive Telegram UI
- Fully Dockerized for easy deployment on any Ubuntu server

---

## 🧱 Requirements

- Docker and Docker Compose installed on your server
- A working Marzneshin panel instance
- A Telegram Bot Token (via [@BotFather](https://t.me/BotFather))
- SUDO admin credentials from Marzneshin panel

---

## ⚡️ One-Line Installation (Recommended)

You can install and run the bot on any Ubuntu server using:

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/lilezza/TrafficBot/main/install_luffybot.sh)"

---

🛠 Manual Setup (Optional)

1. Clone the repository

git clone https://github.com/lilezza/TrafficBot.git
cd TrafficBot

---

2. Create .env file manually

BOT_TOKEN=your-telegram-bot-token
MARZNESHIN_API_BASE_URL=http://your-panel-url:8001

---

3. Build and run the Docker container

docker build -t luffybot .
docker run -d --name luffybot_container --env-file .env luffybot

---

🧾 Project Structure

TrafficBot/
├── api/
├── handlers/
├── middlewares/
├── bot.py
├── state.py
├── Dockerfile
├── install_luffybot.sh
├── requirements.txt
└── .env (ignored via .gitignore)

---

🔐 Security Notes

.env file is ignored via .gitignore and should not be committed to GitHub.
Only SUDO admins from the Marzneshin panel can log in to use the bot.
No chat_id whitelisting is required thanks to credential-based access.

---

🧑‍💻 Author

Made with ❤️ by @lil_rezza
Feel free to fork, contribute or reach out for help

