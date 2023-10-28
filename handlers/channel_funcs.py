from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatJoinRequest, ReplyKeyboardRemove

from keyboards.for_choose_channel import choose_channel_kb
from keyboards.for_start import user_start_kb

from database import Database

router = Router()

database = Database()

@router.chat_join_request()
async def approve_chat_join_request(chat_join: ChatJoinRequest, bot: Bot):
    msg = "Привет! Да, ты наверняка в шоке, ведь боты вроде как не могут " \
          "писать первыми, если им не написать что-то. Но я тебе пишу!" \
          " Твоя заявка в канал принята, все супер :) Выбери по кнопкам ниже, какой материал" \
          " ты бы хотел(-а) получить: "
    await bot.send_message(chat_id=chat_join.from_user.id, text=msg, reply_markup=user_start_kb())
    await chat_join.approve()
    try:
        database.add_user(user=chat_join.from_user, role="follower")
    except Exception as e:
        print(e)

