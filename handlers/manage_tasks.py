from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command

from bot_logging.logger import logger
from database.requests import set_user, add_task_db

router_manage_tasks = Router()


@router_manage_tasks.message(Command('add_task'))
@router_manage_tasks.message(F.text.contains('задание'))
async def add_task(message: types.Message):
    try:
        tg_id = message.from_user.id
        logger.log("info", f"Пользователь вошёл в хэндлер /add_task {tg_id}")
        await set_user(tg_id)
        await message.answer('Напишите название задачи по такому шаблону "название: "')

        @router_manage_tasks.message(F.text.contains('название:'))
        async def process_task_name(message: types.Message):
            task_name = message.text
            await message.answer(f'Вы ввели название задачи: {task_name}')
            await message.answer(
                'Вы можете написать описание, если хотите просто напишете "да", если нет то напишите "закончили"')

            @router_manage_tasks.message(F.text.contains('да'))
            async def process_task_description(message: types.Message):
                await message.answer(
                    f'Хорошо, вы хотите написать описание вашей задачи, напишите пожалуйста его по шаблону "описание:"')

                @router_manage_tasks.message(F.text.contains('описание:'))
                async def process_order_db_description(message: types.Message):
                    try:
                        task_description = message.text
                        await add_task_db(tg_id, task_name, description=task_description)
                    except Exception as e:
                        logger.log("error",
                                   f"Произошла ошибка {str(e)} при записе в бд задачи с описанием у пользователя {tg_id}")

            @router_manage_tasks.message(F.text.contains('закончили'))
            async def add_task_finish(message: types.Message):
                try:
                    await add_task_db(tg_id, task_name)
                except Exception as e:
                    logger.log("error",
                               f"Произошла ошибка {str(e)} при записе в бд задачи без описания у пользователя {tg_id}")
    except Exception as e:
        await logger.log("error", f"Произошла ошибка в хэндлере /add_task{str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
