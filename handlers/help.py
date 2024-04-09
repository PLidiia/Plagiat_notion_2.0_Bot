from aiogram import Router, types, F
from aiogram.filters import Command
from handlers.message import help_cmd_message

router_help = Router()


@router_help.message(Command('help'))
@router_help.message(F.text.contains('помощь'))
async def help_cmd(message: types.Message):
    await message.answer(help_cmd_message)