from loader import bot


async def on_shutdown(dp):
    await bot.delete_webhook()
