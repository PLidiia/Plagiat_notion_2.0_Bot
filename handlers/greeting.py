from aiogram import Router, types, F
from aiogram.filters import CommandStart
from handlers.messages import start_cmd_message_existing, start_cmd_message_not_existing
from database.requests import set_user

router = Router()


@router.message(CommandStart())
@router.message(F.text.contains('старт'))
async def start_cmd(message: types.Message):
    entity = await set_user(message.from_user.id)
    if entity:
        await message.answer(f'{message.from_user.first_name}, {start_cmd_message_existing}')
    else:
        await message.answer(f'{message.from_user.first_name}, {start_cmd_message_not_existing}')
