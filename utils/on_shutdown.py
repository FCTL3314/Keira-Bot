import aiogram

from loader import bot


async def on_shutdown(dp: aiogram.Dispatcher):
    await bot.delete_webhook()
