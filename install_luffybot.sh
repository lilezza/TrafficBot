#!/bin/bash

echo "🧠 Starting LuffyBot installation..."


read -p "🔑 Enter your Telegram Bot Token: " BOT_TOKEN


read -p "🌐 Enter Marzneshin Panel Base URL (e.g., https://panel.example.com:2087): " API_URL


if [ ! -f "Dockerfile" ]; then
  echo "📁 Dockerfile not found. Cloning project from GitHub..."
  git clone https://github.com/lilezza/TrafficBot.git || {
    echo "❌ Failed to clone the repository!"
    exit 1
  }
  cd TrafficBot || exit
else
  echo "✅ Dockerfile found. Continuing installation..."
fi


echo "BOT_TOKEN=$BOT_TOKEN" > .env
echo "MARZNESHIN_API_BASE_URL=$API_URL" >> .env
echo "✅ .env file created."


if ! command -v docker &> /dev/null; then
  echo "❌ Docker is not installed. Please install Docker first: https://docs.docker.com/engine/install/"
  exit 1
fi


docker rm -f luffybot_container 2>/dev/null


echo "🐳 Building Docker image..."
docker build -t luffybot . || {
  echo "❌ Failed to build Docker image!"
  exit 1
}


echo "🚀 Running the bot in background..."
docker run -d --name luffybot_container --env-file .env luffybot || {
  echo "❌ Failed to run Docker container!"
  exit 1
}

echo "🎉 Installation completed successfully! LuffyBot is now running."
