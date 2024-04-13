from aiogram import Router, types, F
from aiogram.filters import Command
from API.hh.graphical_display_vacancies import draw_diagram
from bot_logging.logger import logger
from aiogram.types.input_file import FSInputFile
router_hh = Router()


@router_hh.message(Command('get_diagram_about_job'))
async def get_diagram_about_job(message: types.Message):
    try:
        await message.answer('Введите название профессии по шаблону "профессия: "')

        @router_hh.message(F.text.contains('профессия: '))
        async def get_name_job(message: types.Message):
            await message.answer('Подождите идёт создания графика...')
            job = message.text.split('профессия: ')
            draw_diagram(job)
            await message.answer_photo(FSInputFile('salary_chart.png'))

    except Exception as e:
        logger.log('error', f"Произошла ошибка в хэндлере /get_diagram_about_job {str(e)}")
        await message.answer(
            'Возникла неизвестная ошибка на стороне бота, в течение 6 часов будет решена проблема')
