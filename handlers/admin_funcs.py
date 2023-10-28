from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.user_admin import UserAdminFilter

from keyboards.for_choose_channel import choose_channel_kb
from keyboards.for_choose_user import choose_user_kb, yes_no_kb
from keyboards.for_start import admin_start_kb

from config_reader import config

from database import Database

router = Router()

database = Database()


class SelectingChannels(StatesGroup):
    selecting_main_channel = State()
    selecting_reserve_channel = State()


@router.message(
    UserAdminFilter(user_role=["admin"]),
    F.text.lower() == "назад в главное меню"
)
async def cmd_main_admin_menu(message: Message):
    await message.answer("Что будем делать?", reply_markup=admin_start_kb(admin_type="admin"))

@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    F.text.lower() == "назад в главное меню"
)
async def cmd_main_admin_menu(message: Message):
    await message.answer("Что будем делать?", reply_markup=admin_start_kb(admin_type="superadmin"))


@router.message(Command(config.secret_admin_key.get_secret_value()))
async def cmd_secret_key(message: Message):
    await message.answer("Привет, супер-админ!")
    try:
        new_admin = database.add_user(message.from_user, role="superadmin")
    except Exception as e:
        print(e)


@router.message(
    UserAdminFilter(user_role=["admin", "superadmin"]),
    Command("start")
)
async def cmd_admin_start(message: Message):
    admin_role = database.get_user_role(message.from_user.id)
    await message.answer("Привет! Что будем делать?", reply_markup=admin_start_kb(admin_type=admin_role))


@router.message(
    UserAdminFilter(user_role=["admin", "superadmin"]),
    Command("swap_channel")
)
async def cmd_swap_channel(message: Message):
    await message.answer("Канал открыт!")