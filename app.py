import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv.main import load_dotenv

from common.bot_cmd_list import commands
from handlers.greeting import router
from handlers.help import router_help
from database.models import create_tables

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()
dp.include_router(router)
dp.include_router(router_help)


async def main():
    await bot.set_my_commands(commands=commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await create_tables()
    await dp.start_polling(bot)


asyncio.run(main())
