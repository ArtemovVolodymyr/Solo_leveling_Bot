# core/daily_reset.py
import asyncio
import datetime
import logging
from core.storage import load_players, save_players
from aiogram import Bot

async def start_daily_reset_task(bot: Bot):
    while True:
        now = datetime.datetime.now()
        next_day = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (next_day - now).total_seconds()
        if wait_seconds <= 0:
            wait_seconds = 60
        await asyncio.sleep(wait_seconds)
        players = load_players()
        for uid, p in players.items():
            p['done_actions'] = []
            if 'daily' in p:
                for k in p['daily']:
                    p['daily'][k] = False
            try:
                await bot.send_message(int(uid), "🕛 Дневные действия и победы сброшены! Новый день начинается!")
            except Exception as e:
                logging.warning(f"Не удалось уведомить {uid}: {e}")
        save_players(players)
        logging.info("Сброс дневных действий и побед выполнен.")
