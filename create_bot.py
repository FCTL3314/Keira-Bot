import aiogram

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from configurations.config import TOKEN

storage = MemoryStorage()
user_data = {}
bot_data = {}

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot=bot)
