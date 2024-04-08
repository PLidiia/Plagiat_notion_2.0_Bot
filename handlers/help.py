from aiogram import Router, types
from aiogram.filters import Command
from handlers.message import help_cmd_message

router_help = Router()


@router_help.message(Command('help'))
async def help_cmd(message: types.Message):
    await message.answer(help_cmd_message)