from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_logging.logger import logger
from database.requests import set_user, show_tasks_db
from handlers.text_keyboard_builder import builder_add_task_name, builder_add_task_description

router_manage_tasks = Router()


@router_manage_tasks.message(Command('add_task'))
@router_manage_tasks.message(F.text.contains('задание'))
async def add_task(message: types.Message):
    try:
        tg_id = message.from_user.id
        logger.log("info", f"Пользователь вошёл в хэндлер /add_task {tg_id}")
        await set_user(tg_id)
        name_keyboard = InlineKeyboardBuilder()
        name_keyboard.add(
            InlineKeyboardButton(text=builder_add_task_name[0],
                                 callback_data=builder_add_task_name[0]))
        kb_name = name_keyboard.as_markup()
        await message.answer("Начинаем заполнять задачу", reply_markup=kb_name)

        @router_manage_tasks.callback_query()
        async def save_name(callback: types.CallbackQuery):

            description_keyboard = InlineKeyboardBuilder()
            for active in builder_add_task_description:
                name_keyboard.add(
                    InlineKeyboardButton(text=active,
                                         callback_data=active))
                kb = description_keyboard.as_markup()
                await callback.message.answer("Что насчёт описания задачи???", reply_markup=kb)

                @router_manage_tasks.callback_query(F.data == str(builder_add_task_description[0]))
                async def save_task_with_description(callback: types.CallbackQuery):
                    print('fffffff')
                    task_description = callback.data
                    await add_task(tg_id, task_name, task_description)

                @router_manage_tasks.callback_query(F.data == builder_add_task_description[1])
                async def save_task_without_description(callback: types.CallbackQuery):
                    await add_task(tg_id, task_name)

    except Exception as e:
        logger.log("error", f"Произошла ошибка в хэндлере /add_task {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')


@router_manage_tasks.message(Command('show_my_tasks'))
@router_manage_tasks.message(F.text.contains('покажи мои задания'))
@router_manage_tasks.message(F.text.contains('мои задания'))
@router_manage_tasks.message(F.text.contains('мои задачи'))
async def show_my_tasks(message: types.Message):
    try:
        tg_id = message.from_user.id
        logger.log("info", f"Пользователь вошёл в хэндлер /show_my_tasks {tg_id}")
        tasks = await show_tasks_db(tg_id)
        if tasks:
            tasks_key_board = InlineKeyboardBuilder()
            if len(tasks) <= 100:
                # venv/Lib/site-packages/aiogram/utils/keyboard.py:299
                # в библиотеке aiogram есть предел для инлайновых кнопок в конструктуре - это 100
                for task in tasks:
                    tasks_key_board.add(
                        InlineKeyboardButton(text=task.name,
                                             callback_data=f'task_{task.name}'))
                kb = tasks_key_board.adjust(2).as_markup()
                await message.answer("Вот ваши задачи:", reply_markup=kb)
            else:
                await message.answer("К сожалению, библиотека aiogram не может вывести такое количество задач, "
                                     "в отличие от вас, воспользуйтесь  /delete_task")
        else:
            await message.answer("Вы ещё не создавали задачи, обратитесь к хэндлеру /add_task")
    except Exception as e:
        logger.log("error", f"Произошла ошибка в хэндлере /show_my_tasks {str(e)}")
        await message.answer('Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')


@router_manage_tasks.callback_query()
async def edit_task(callback: types.CallbackQuery):
    try:
        if 'task_' in callback.data:
            id_task = callback.data.split('_')[1]
            await callback.answer(f'{id_task}')
            await callback.message.answer(f'Вы выбрали задачу, что вы хотите с ней сделать?')
    except Exception as e:
        logger.log("error", f"Произошла ошибка в обработчике нажатий в конструктуре задач (функция edit_task) {str(e)}")
        await callback.message.answer(
            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
