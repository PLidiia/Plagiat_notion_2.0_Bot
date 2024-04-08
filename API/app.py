import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv.main import load_dotenv

from handlers.greeting import router


load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
