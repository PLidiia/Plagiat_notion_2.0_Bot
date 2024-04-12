from aiogram import Router, types, F
from aiogram.filters import CommandStart

from bot_logging.logger import logger
from database.requests import set_user
from handlers.messages import start_cmd_message_existing, start_cmd_message_not_existing

router = Router()


@router.message(CommandStart())
@router.message(F.text.contains('старт'))
async def start_cmd(message: types.Message):
    try:
        logger.log("info", "Запущен хэндлер /start")
        entity = await set_user(message.from_user.id)
        if entity:
            logger.log("info", f"{message.from_user.first_name} - пользователь уже заходил в бота")
            await message.answer(f'{message.from_user.first_name}, {start_cmd_message_existing}')
        else:
            logger.log("info", f"{message.from_user.first_name} - пользователь не заходил в бота")
            await message.answer(f'{message.from_user.first_name}, {start_cmd_message_not_existing}')
    except Exception as e:
        logger.log("error", f"ошибка в хэндлере /start {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
