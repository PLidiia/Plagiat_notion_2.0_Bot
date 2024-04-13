import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv.main import load_dotenv

from common.bot_cmd_list import commands
from database.models import create_tables
from handlers.greeting import router
from handlers.help import router_help
from handlers.hh_info import router_hh
from handlers.manage_tasks import router_manage_tasks

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()
dp.include_router(router)
dp.include_router(router_help)
dp.include_router(router_manage_tasks)
dp.include_router(router_hh)


async def main():
    await bot.set_my_commands(commands=commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await create_tables()
    await dp.start_polling(bot)


asyncio.run(main())
