from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command

from database.requests import set_user, add_task_db

router_manage_tasks = Router()


@router_manage_tasks.message(Command('add_task'))
@router_manage_tasks.message(F.text.contains('задание'))
async def add_task(message: types.Message):
    tg_id = message.from_user.id
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
            task_description = message.text
            await message.answer(f'Вы ввели описание задачи: {task_description}')
            await add_task_db(tg_id, task_name, description=task_description)

        @router_manage_tasks.message(F.text.contains('закончили'))
        async def add_task_finish(message: types.Message):
            await add_task_db(tg_id, task_name)
