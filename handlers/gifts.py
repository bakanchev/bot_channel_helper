from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_start import user_start_kb

from aiogram import F

router = Router()

"""

это просто команды-заглушки, здесь конечно можно развивать идею дальше, 
создавать БД с хранением файлов и так далее

"""

@router.message(Command("start"))
async def cmd_user_start(message: Message):
    await message.answer(
        "Привет! Какой подарок выберешь?",
        reply_markup=user_start_kb()
    )

@router.message(F.text.lower() == "полезный файл")
async def cmd_user_want_file(message: Message):
    await message.answer(
        "Держи файл по основам программирования",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "промокод на курс")
async def cmd_user_want_promocode(message: Message):
    await message.answer(
        "Вот очень крутой промокод на курс по программированию: ABCDEFG",
        reply_markup=ReplyKeyboardRemove()
    )