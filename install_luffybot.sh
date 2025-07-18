#!/bin/bash

echo "🧠 نصب ربات LuffyBot در حال اجراست..."

read -p "🔑 توکن ربات را وارد کنید: " BOT_TOKEN
read -p "🌐 آدرس پنل مرزنشین را وارد کنید (مثلاً http://192.168.1.10:8001): " API_URL

cat > .env <<EOL
BOT_TOKEN=$BOT_TOKEN
MARZNESHIN_API_BASE_URL=$API_URL
EOL

echo "✅ فایل .env ساخته شد."

echo "🐳 ساخت ایمیج Docker..."
docker build -t luffybot .

echo "🚀 اجرای ربات در پس‌زمینه..."
docker run -d --name luffybot_container --env-file .env luffybot

echo "🎉 نصب با موفقیت انجام شد!"
