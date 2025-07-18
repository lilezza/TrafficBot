import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.auth_middleware import AuthMiddleware
from middlewares.session_middleware import SessionMiddleware
from dotenv import load_dotenv
from handlers import router as main_router


load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

dp.update.middleware(SessionMiddleware())
dp.message.middleware(AuthMiddleware())
dp.callback_query.middleware(AuthMiddleware())

dp.include_router(main_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
