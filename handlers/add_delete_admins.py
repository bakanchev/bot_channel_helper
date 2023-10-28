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


class AddingAdmin(StatesGroup):
    choosing_admin = State()
    confirming_adding_admin = State()


class DeletingAdmin(StatesGroup):
    choosing_deleting_admin = State()
    confirming_deleting_admin = State()

@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    F.text.lower() == "добавить админа"
)
async def cmd_add_admin(message: Message, state: FSMContext):
    await message.answer(
        "Кого хотите добавить в админы?",
        reply_markup=choose_user_kb()
    )
    await state.set_state(AddingAdmin.choosing_admin)

@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    AddingAdmin.choosing_admin,
    F.user_shared
)
async def admin_chosen(message: Message, state: FSMContext):
    await state.update_data(admin_chosen=message.user_shared.user_id)
    if database.get_user_role(message.user_shared.user_id) not in ["admin", "superadmin"]:
        await message.answer(
            text=f"Подтверждаете выбор этого человека в качестве админа?",
            reply_markup=yes_no_kb()
        )
        await state.set_state(AddingAdmin.confirming_adding_admin)
    else:
        await message.answer(
            text=f"Этот человек уже является админом.\nПопробуйте выбрать другого пользователя.",
            reply_markup=choose_user_kb()
        )


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    AddingAdmin.confirming_adding_admin,
    F.text.lower() == "да"
)
async def admin_confirming(message: Message, state: FSMContext):
    user_data = await state.get_data()
    admin_id = user_data['admin_chosen']
    if database.add_admin(admin_id, "admin"):
        await message.answer(
            text=f"Новый админ успешно добавлен.\n",
            reply_markup=admin_start_kb(admin_type="superadmin")
        )
        await state.clear()
    else:
        await message.answer(
            text=f"Админа добавить не получилось.\n"
                 "Попробуйте еще раз:",
            reply_markup=choose_user_kb()
        )



@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    AddingAdmin.confirming_adding_admin,
    F.text.lower() == "нет"
)
async def admin_not_confirming(message: Message, state: FSMContext):
    await message.answer(
        "Кого хотите добавить в админы?",
        reply_markup=choose_user_kb()
    )
    await state.set_state(AddingAdmin.choosing_admin)


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    F.text.lower() == "удалить админа"
)
async def cmd_delete_admin(message: Message, state: FSMContext):
    await message.answer(
        "Кого хотите удалить из админов?",
        reply_markup=choose_user_kb()
    )
    await state.set_state(DeletingAdmin.choosing_deleting_admin)

@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    DeletingAdmin.choosing_deleting_admin,
    F.user_shared
)
async def admin_deleted_chosen(message: Message, state: FSMContext):
    await state.update_data(admin_chosen=message.user_shared.user_id)
    if database.get_user_role(message.user_shared.user_id) not in ["admin", "superadmin"]:
        await message.answer(
            text=f"Этот пользователь не является админом.\nПопробуйте еще раз.",
            reply_markup=choose_user_kb()
        )
    else:
        await message.answer(
            text=f"Вы уверены, что хотите удалить этого пользователя из админов?",
            reply_markup=yes_no_kb()
        )
        await state.set_state(DeletingAdmin.confirming_deleting_admin)


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    DeletingAdmin.confirming_deleting_admin,
    F.text.lower() == "да"
)
async def admin_deleting_confirming(message: Message, state: FSMContext):
    user_data = await state.get_data()
    admin_id = user_data['admin_chosen']
    if F.text.lower() == "да":
        if database.change_user_role(admin_id, "follower"):
            await message.answer(
                text=f"Админ успешно удален.\n",
                reply_markup=admin_start_kb(admin_type="superadmin")
            )
        else:
            await message.answer(
                text=f"Админа удалить не получилось.\n"
                     "Попробуйте еще раз.",
                reply_markup=choose_user_kb()
            )
        await state.set_state(DeletingAdmin.choosing_deleting_admin)


@router.message(
    UserAdminFilter(user_role=["superadmin"]),
    DeletingAdmin.confirming_deleting_admin,
    F.text.lower() == "нет"
)
async def admin_deleting_not_confirming(message: Message, state: FSMContext):
    await message.answer(
        "Кого хотите удалить из админов?",
        reply_markup=choose_user_kb()
    )
    await state.set_state(DeletingAdmin.choosing_deleting_admin)
