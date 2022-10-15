import utils.sql

from loader import bot
from data.config import WEBHOOK_URL


async def on_startup(dp):
    print('*START*')
    await bot.set_webhook(WEBHOOK_URL)
    with utils.sql.database as db:
        db.create_table()
