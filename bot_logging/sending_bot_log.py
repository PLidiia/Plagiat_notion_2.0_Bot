import asyncio
import os

from aiogram import BaseMiddleware
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv.main import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_LOGGER")

hello_router = Router(name='hello')


def get_data_log_file() -> str:
    with open('telegram_bot.txt', 'r') as logfile:
        data = logfile.readlines()
        clear_data = ''
        for item in data:
            clear_data = clear_data + item + '\n'
        return clear_data


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        data["scheduler"] = self._scheduler
        return await handler(event, data)


@hello_router.message(CommandStart())
async def hello(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
    id = message.from_user.id
    data = get_data_log_file()
    scheduler.add_job(bot.send_message, 'interval', hours=6, args=(id, str(data)))


async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.include_routers(hello_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
