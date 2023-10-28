from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union

from database import Database


class UserAdminFilter(BaseFilter):
    def __init__(self, user_role: Union[str, list]):
        self.user_role = user_role

    async def __call__(self, message: Message) -> bool:
        database = Database()
        if isinstance(self.user_role, str):
            return database.get_user_role(message.from_user.id) == self.user_role
        else:
            return database.get_user_role(message.from_user.id) in self.user_role
