from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import random


def yes_no_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def choose_user_kb() -> types.ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(
            request_user=types.KeyboardButtonRequestUser(
                request_id=random.randint(-(2**31), (2**31) - 1),
            ),
            text="Выбрать человека",
        )
    )
    kb.button(text="Назад в главное меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)