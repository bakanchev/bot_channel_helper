from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.user_admin import UserAdminFilter
from filters.custom import bot_is_admin

from keyboards.for_choose_channel import choose_channel_kb
from keyboards.for_start import return_to_main_kb
from keyboards.for_start import admin_start_kb

from config_reader import config

from database import Database

router = Router()

database = Database()


class SelectingChannels(StatesGroup):
    selecting_main_channel = State()
    selecting_reserve_channel = State()


class SelectingOffer(StatesGroup):
    selecting_offer = State()


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    F.text.lower() == "настроить каналы"
)
async def cmd_setup_channels(message: Message, state: FSMContext):
    await message.answer(
        "Начнем настройку каналов.\n"
        "Вам необходимо будет сначала указать основной канал, на который будут приходить подписчики "
        "(чтобы затем его сделать закрытым с входом по заявкам), а также резервный канал, который "
        "сможет сохранить публичную ссылку вашего канала, чтобы ее не занял кто-то другой.",
        reply_markup=choose_channel_kb(channel_type="main")
    )
    await state.set_state(SelectingChannels.selecting_main_channel)


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    SelectingChannels.selecting_main_channel,
    F.chat_shared
)
async def main_channel_chosen(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(channel_chosen=message.chat_shared.chat_id)
    try:
        if database.add_channel(message.chat_shared.chat_id, "main"):
            if not await bot_is_admin(bot, chat_id=message.chat_shared.chat_id):
                await message.answer(
                    text=f"Бот не является администратором в этом канале.\n"
                         "Повторите установку",
                    reply_markup=return_to_main_kb()
                )
                await state.clear()
            else:
                await message.answer(
                    text=f"Канал успешно выбран в качестве основного. Теперь установите резервный канал:",
                    reply_markup=choose_channel_kb(channel_type="reserve")
                )
                await state.set_state(SelectingChannels.selecting_reserve_channel)
        else:
            await message.answer(
                text=f"Установить основной канал не получилось, попробуйте снова.",
                reply_markup=choose_channel_kb(channel_type="main")
            )
            await state.set_state(SelectingChannels.selecting_main_channel)

    except Exception as e:
        print(e)


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    SelectingChannels.selecting_reserve_channel,
    F.chat_shared
)
async def reserve_channel_chosen(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(channel_chosen=message.chat_shared.chat_id)
    try:
        if database.add_channel(message.chat_shared.chat_id, "reserve"):
            if not await bot_is_admin(bot, chat_id=message.chat_shared.chat_id):
                await message.answer(
                    text=f"Бот не является администратором в этом резервном канале.\n"
                         "Повторите установку",
                    reply_markup=return_to_main_kb()
                )
                await state.clear()
            else:
                await message.answer(
                    text=f"Канал успешно выбран в качестве резервного."
                         "Теперь можно настроить оффер (описание, которое "
                         "будут видеть юзеры в момент подачи заявки на вступление в канал).\n\n"
                         "Чтобы настроить оффер, пришлите мне его в ответном сообщении.\n"
                         "Например, можно написать так:\n\n"
                         "Чтобы получить крутой файл по программированию с нуля, подавай заявку"
                         " на вступление в канал! Жми кнопку ⬇️ ⬇️ ⬇️",
                    reply_markup=return_to_main_kb()
                )

                await state.set_state(SelectingOffer.selecting_offer)
        else:
            await message.answer(
                text=f"Установить резервный канал не получилось, попробуйте снова.",
                reply_markup=choose_channel_kb(channel_type="reserve")
            )
            await state.set_state(SelectingChannels.selecting_reserve_channel)

    except Exception as e:
        print(e)


@router.message(
    UserAdminFilter(user_role=["superadmin", "admin"]),
    SelectingOffer.selecting_offer
)
async def offer_sent(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(offer=message.text)
    reserve_channel_id = database.get_channel_id_by_type("reserve")
    try:
        result = await bot.set_chat_description(chat_id=reserve_channel_id, description=message.text)
        if result:
            await message.answer(
                text=f"Оффер успешно установлен в описании резервного канала!",
                reply_markup=admin_start_kb(admin_type="admin")
            )

            await state.clear()
        else:
            await message.answer(
                text=f"Оффер установить не получилось!\n"
                     "Убедитесь, что символов в описании не больше 255 и повторите попытку.",
                reply_markup=return_to_main_kb()
            )
    except Exception as e:
        print(e)


@router.message(
    UserAdminFilter(user_role=["superadmin", "admin"]),
    F.text.lower() == "настроить оффер"
)
async def cmd_set_offer(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text=f"Чтобы настроить оффер (описание, которое "
             "будут видеть юзеры в момент подачи заявки на вступление в канал),"
             " пришлите мне его в ответном сообщении. "
             "Например, можно написать так:\n\n"
             "Чтобы получить крутой файл по программированию с нуля, подавай заявку"
             " на вступление в канал! Жми кнопку ⬇️ ⬇️ ⬇️",
        reply_markup=return_to_main_kb()
    )

    await state.set_state(SelectingOffer.selecting_offer)
