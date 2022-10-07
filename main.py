import aiogram
import src

from create_bot import dp


def main():
    print('***start***')
    src.start_command.register_start_command_handlers(dp=dp)
    src.achievements_command.register_achievements_command_handlers(dp=dp)

    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)


if __name__ == '__main__':
    main()
