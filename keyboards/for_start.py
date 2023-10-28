from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


superadmin_commands = [""]

def user_start_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Полезный файл")
    kb.button(text="Промокод на курс")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def admin_start_kb(admin_type: str) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Настроить оффер")
    )
    if admin_type == "superadmin":
        builder.row(
            types.KeyboardButton(text="Добавить админа"),
            types.KeyboardButton(text="Удалить админа")
        )
        builder.row(
            types.KeyboardButton(text="Настроить каналы")
        )
    return builder.as_markup(resize_keyboard=True)

def return_to_main_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад в главное меню")
    return kb.as_markup(resize_keyboard=True)