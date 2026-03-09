"""
Telegram-бот доставки пиццы.
Запуск: python bot.py
"""
import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db
from handlers import user_router, order_router, admin_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main():
    """Запуск бота."""
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "Установите BOT_TOKEN! Создайте config/local_config.py с BOT_TOKEN "
            "или задайте переменную окружения BOT_TOKEN."
        )
        return

    # Инициализация БД
    init_db()
    logger.info("База данных инициализирована.")

    # Создание бота и диспетчера
    try:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        )
    except TokenValidationError:
        logger.error(
            "Неверный BOT_TOKEN! Проверьте токен в config/local_config.py. "
            "Получите новый токен у @BotFather."
        )
        return
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(user_router)
    dp.include_router(order_router)
    dp.include_router(admin_router)

    # Запуск polling (drop_pending_updates — не обрабатывать старые апдейты при старте)
    logger.info("Бот запущен!")
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
