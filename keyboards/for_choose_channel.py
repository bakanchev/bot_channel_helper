from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import random

def choose_channel_kb(channel_type: str) -> types.ReplyKeyboardMarkup:
    channel_types = {
        "reserve": "резервный",
        "main": "основной"
    }
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(
            request_chat=types.KeyboardButtonRequestChat(
                request_id=random.randint(-(2**31), (2**31) - 1),
                user_administrator_rights=types.ChatAdministratorRights(
                    is_anonymous=True,
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_invite_users=True
                ),
                bot_administrator_rights=types.ChatAdministratorRights(
                    is_anonymous=True,
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=True,
                    can_invite_users=True
                ),
                chat_is_channel=True,
                bot_is_member=True
            ),
            text=f"Выбрать {channel_types[channel_type]} канал",
        )
    )
    kb.button(text="Назад в главное меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)