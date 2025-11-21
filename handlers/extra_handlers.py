# handlers/extra_handlers.py
from aiogram import types
from loader import dp
from core.storage import get_player, load_players
from core.visual import exp_bar_emoji
from config.settings import OWNER_ID

@dp.message_handler(lambda m: m.text == '🏆 Достижения')
async def menu_achievements(message: types.Message):
    player = get_player(message.from_user)
    ach = player.get('achievements', [])
    if not ach:
        await message.reply("У вас ещё нет достижений 🏅")
    else:
        ach_texts = []
        for a in ach:
            if a == 'first_level':
                ach_texts.append("🎉 Первый уровень!")
            elif a == '10_actions':
                ach_texts.append("✅ Выполнено 10 действий!")
            else:
                ach_texts.append(f"🏆 {a}")
        await message.reply("Ваши достижения:\n" + "\n".join(ach_texts))

@dp.message_handler(lambda m: m.text == '🕒 История 7д')
async def history_7d(message: types.Message):
    player = get_player(message.from_user)
    import datetime
    now = datetime.datetime.utcnow()
    week_ago = now - datetime.timedelta(days=7)
    hist = [h for h in player.get('action_history', []) if datetime.datetime.fromisoformat(h['ts']) >= week_ago]
    if not hist:
        await message.reply("За последние 7 дней действий не найдено.")
        return
    by_day = {}
    for h in hist:
        dt = datetime.datetime.fromisoformat(h['ts'])
        day = dt.date().isoformat()
        by_day.setdefault(day, []).append(h)
    lines = []
    for day in sorted(by_day.keys(), reverse=True):
        lines.append(f"📅 {day}:")
        for h in by_day[day]:
            ts = datetime.datetime.fromisoformat(h['ts']).strftime("%H:%M")
            lines.append(f"  - {ts}  {h['action']}")
    await message.reply("\n".join(lines))

@dp.message_handler(commands=['dump'])
async def cmd_dump(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.reply("Только админ может использовать эту команду.")
        return
    filename = "players_dump.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(load_players(), f, ensure_ascii=False, indent=4)
    await message.reply_document(types.InputFile(filename))
    try:
        os.remove(filename)
    except Exception:
        pass
