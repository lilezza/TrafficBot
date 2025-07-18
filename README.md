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
