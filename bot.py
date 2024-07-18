import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import API_TOKEN
from handlers.achievements_handlers import register_handlers as register_achievement_handlers
from handlers.auth_handlers import register_auth_handlers
from database import init_db

logging.basicConfig(level=logging.INFO)

bot_instance = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot_instance, storage=storage)
dp.middleware.setup(LoggingMiddleware())

register_auth_handlers(dp, bot_instance)
register_achievement_handlers(dp, bot_instance)

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
