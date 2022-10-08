import aiogram
import data

from aiogram.contrib.fsm_storage.memory import MemoryStorage

user_data = {}
bot_data = {}

storage = MemoryStorage()

bot = aiogram.Bot(token=data.config.TOKEN)
dp = aiogram.Dispatcher(bot=bot, storage=storage)
