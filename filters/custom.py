from aiogram import Bot


async def bot_is_admin(bot: Bot, chat_id: int) -> bool:
    try:
        members = await bot.get_chat_administrators(chat_id=chat_id)
        return any(x.user.id == bot.id for x in members)
    except Exception as e:
        print(e)
