# keyboards/actions_keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.categories import CATEGORIES
from data.actions import ACTIONS
from core.visual import short_action_button_text
from config.settings import PAGE_SIZE

def action_categories_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    for key, name in CATEGORIES.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"category::{key}::0"))
    return kb

def actions_list_keyboard(category_key: str, player: dict, page: int = 0):
    items = [name for name, info in ACTIONS.items() if info['category'] == category_key]
    items.sort()
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    kb = InlineKeyboardMarkup(row_width=1)
    for name in items[start:end]:
        kb.add(InlineKeyboardButton(short_action_button_text(name, ACTIONS[name]), callback_data=f"choose::{name}"))
    total_pages = max(1, (len(items) + PAGE_SIZE - 1) // PAGE_SIZE)
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"category::{category_key}::{page-1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton("Вперёд ➡️", callback_data=f"category::{category_key}::{page+1}"))
    if nav:
        kb.row(*nav)
    kb.add(InlineKeyboardButton("🔙 Категории", callback_data="categories::0"))
    return kb
