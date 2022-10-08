import aiogram

from configurations.config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

user_data = {}
bot_data = {}

storage = MemoryStorage()

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot=bot, storage=storage)
