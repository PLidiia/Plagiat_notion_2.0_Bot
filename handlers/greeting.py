from aiogram import Router, types, F
from aiogram.filters import CommandStart
from handlers.message import start_cmd_message
router = Router()


@router.message(CommandStart())
@router.message(F.text.contains('старт'))
async def start_cmd(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, {start_cmd_message}')
