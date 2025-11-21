# handlers/actions_handlers.py
import datetime
import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from core.storage import get_player, save_player_for_user, load_players
from core.visual import short_action_button_text, exp_bar_emoji
from core.progression import add_exp
from core.achievements import check_achievements
from data.actions import ACTIONS
from data.categories import CATEGORIES
from keyboards.actions_keyboards import action_categories_keyboard, actions_list_keyboard

def format_seconds(sec:int) -> str:
    if sec <= 0:
        return "0s"
    days, sec = divmod(sec, 86400)
    hours, sec = divmod(sec, 3600)
    minutes, sec = divmod(sec, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if sec and not parts:
        parts.append(f"{sec}s")
    return ' '.join(parts)

@dp.message_handler(lambda m: m.text == '🎯 Действия')
async def menu_quests(message: types.Message):
    await message.reply("Выберите категорию действий:", reply_markup=action_categories_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith("categories::"))
async def back_to_categories(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите категорию действий:", reply_markup=action_categories_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith("category::"))
async def process_category(callback: types.CallbackQuery):
    _, key, page_s = callback.data.split("::")
    page = int(page_s)
    player = get_player(callback.from_user)
    kb = actions_list_keyboard(key, player, page)
    text = f"Категория: {CATEGORIES.get(key,'?')}\nВыберите действие:"
    await callback.message.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("choose::"))
async def process_choose_action(callback: types.CallbackQuery):
    action_name = callback.data.split("::",1)[1]
    player = get_player(callback.from_user)
    info = ACTIONS.get(action_name)
    now = datetime.datetime.utcnow()
    last_done_iso = player.get('last_done', {}).get(action_name)
    can_do = True
    remaining = 0
    if last_done_iso:
        last_done = datetime.datetime.fromisoformat(last_done_iso)
        cd = info.get('cooldown', 0)
        delta = (now - last_done).total_seconds()
        if delta < cd:
            can_do = False
            remaining = int(cd - delta)
    kb = InlineKeyboardMarkup(row_width=2)
    if can_do:
        kb.add(InlineKeyboardButton("Подтвердить ✔️", callback_data=f"do::{action_name}"),
            InlineKeyboardButton("Отмена ❌", callback_data="categories::0"))
    else:
        kb.add(InlineKeyboardButton(f"Осталось: {format_seconds(remaining)}", callback_data="categories::0"))
    text = f"Действие: {action_name}\n{info.get('stat','')} +{info.get('stat_gain',0)} к {info.get('stat')}\nEXP: +{info.get('exp')}\n"
    if not can_do:
        text += f"\n⚠️ Это действие доступно не сразу. Осталось: {format_seconds(remaining)}"
    await callback.message.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("do::"))
async def process_action(callback: types.CallbackQuery):
    action_name = callback.data.split("::",1)[1]
    player = get_player(callback.from_user)
    info = ACTIONS.get(action_name)
    now = datetime.datetime.utcnow()
    last_done_iso = player.get('last_done', {}).get(action_name)
    if last_done_iso:
        last_done = datetime.datetime.fromisoformat(last_done_iso)
        cd = info.get('cooldown', 0)
        delta = (now - last_done).total_seconds()
        if delta < cd:
            await callback.message.answer(f"⚠️ Эту задачу ещё нельзя выполнить. Осталось: {format_seconds(int(cd-delta))}")
            return
    # apply changes
    lvl_msgs = add_exp(player, info['exp'])
    stat = info.get('stat')
    player['stats'][stat] = player['stats'].get(stat, 0) + info.get('stat_gain', 0)
    player.setdefault('last_done', {})[action_name] = now.isoformat()
    if action_name not in player.get('done_actions', []):
        player['done_actions'].append(action_name)
    player.setdefault('action_history', []).append({"action": action_name, "ts": now.isoformat()})
    ach_msgs = check_achievements(player)
    save_player_for_user(callback.from_user.id, player)
    base_text = f"✔️ Выполнено: *{action_name}*\n+{info['exp']} EXP\n{stat} +{info.get('stat_gain',0)}\n"
    if ach_msgs:
        base_text += "\n" + "\n".join(ach_msgs)
    sent = await callback.message.edit_text(base_text + "\n\nОбновляю уровень...", parse_mode="Markdown")
    if lvl_msgs:
        for i in range(3):
            try:
                await asyncio.sleep(0.5)
                await callback.message.edit_text(base_text + "\n\n" + exp_bar_emoji(player, length=8) + f"\n{lvl_msgs[0]}", parse_mode="Markdown")
            except Exception:
                pass
        try:
            await callback.message.edit_text(base_text + "\n\n" + exp_bar_emoji(player) + "\n" + "\n".join(lvl_msgs), parse_mode="Markdown")
        except Exception:
            pass
    else:
        try:
            await callback.message.edit_text(base_text + "\n\n" + exp_bar_emoji(player), parse_mode="Markdown")
        except Exception:
            pass
