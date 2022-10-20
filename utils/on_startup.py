import aiogram
import utils.database

from loader import bot
from data.config import WEBHOOK_URL


async def on_startup(dp):
    await bot.set_my_commands([
        aiogram.types.BotCommand('start', 'Начальная информация.'),
        aiogram.types.BotCommand('set', 'Указать изучаемые слова.'),
        aiogram.types.BotCommand('library', 'Библиотека твоих слов.'),
        aiogram.types.BotCommand('stop', 'Перестать переводить.')
    ])
    await bot.set_webhook(WEBHOOK_URL)
    with utils.database.postgres_database as db:
        db.create_table()
