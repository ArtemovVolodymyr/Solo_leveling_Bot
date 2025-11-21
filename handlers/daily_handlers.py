# handlers/daily_handlers.py
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from core.storage import get_player, save_player_for_user
from core.visual import daily_progress_bar_emoji

@dp.message_handler(lambda m: m.text == '✅ Дневные победы')
async def menu_daily(message: types.Message):
    player = get_player(message.from_user)
    kb = InlineKeyboardMarkup(row_width=2)
    for key in ['financial','mental','physical','personal']:
        kb.add(InlineKeyboardButton(f"{key.capitalize()} [{'✓' if player['daily'].get(key) else ' '}]", callback_data=f"daily::{key}"))
    text = f"Отметь 4 победы дня:\nПрогресс: {daily_progress_bar_emoji(player)}"
    await message.reply(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("daily::"))
async def process_daily(callback: types.CallbackQuery):
    _, key = callback.data.split("::")
    player = get_player(callback.from_user)
    player['daily'][key] = not player['daily'].get(key, False)
    save_player_for_user(callback.from_user.id, player)
    await callback.message.edit_text(f"Отметки обновлены.\nПрогресс: {daily_progress_bar_emoji(player)}", reply_markup=callback.message.reply_markup)
