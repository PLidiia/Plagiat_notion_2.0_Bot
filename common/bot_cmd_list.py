from aiogram.types import BotCommand

commands = [
    BotCommand(command='help', description='Где найти все методы'),
    BotCommand(command='start', description='Что делает бот'),
    BotCommand(command='add_task', description='Добавить задачу'),
    BotCommand(command='show_my_tasks', description='Показать задачи')
]