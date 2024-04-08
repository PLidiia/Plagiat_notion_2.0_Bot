from aiogram import Router, types
from aiogram.filters import Command


router_help = Router()


@router_help.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer('Воспользуйся меню')