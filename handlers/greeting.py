from aiogram import Router, types
from aiogram.filters import CommandStart
from handlers.message import start_cmd_message
router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(start_cmd_message)
