# handlers/start_menu.py
from aiogram import types
from keyboards.main_menu import main_menu_keyboard
from core.storage import get_player
from loader import dp

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    get_player(message.from_user)
    await message.reply("Привет! Я Solo-Leveling бот.", reply_markup=main_menu_keyboard())
