import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from handlers import start_funcs, channel_funcs, admin_funcs, gifts, add_delete_admins, set_channels

from config_reader import config

# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        admin_funcs.router,
        add_delete_admins.router,
        set_channels.router,
        gifts.router,
        start_funcs.router,
        channel_funcs.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(main())
