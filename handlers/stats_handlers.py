# handlers/stats_handlers.py
from aiogram import types
from core.storage import get_player
from core.visual import format_stats, exp_bar_emoji, daily_progress_bar_emoji
from loader import dp

@dp.message_handler(lambda m: m.text == '📊 Статы')
async def menu_stats(message: types.Message):
    p = get_player(message.from_user)
    text = (f"👤 {p.get('name')}\n📈 Level: {p['level']} {exp_bar_emoji(p)}\n\n{format_stats(p)}\n\n"
            f"Дневной прогресс: {daily_progress_bar_emoji(p)}")
    await message.reply(text)

@dp.message_handler(lambda m: m.text == '📈 Уровень')
async def menu_level(message: types.Message):
    p = get_player(message.from_user)
    await message.reply(f"📈 Уровень: {p['level']}\n{exp_bar_emoji(p)}")
