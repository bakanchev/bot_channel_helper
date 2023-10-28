from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_start import user_start_kb
from config_reader import config

from database import Database

router = Router()


