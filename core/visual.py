# core/visual.py
from data.constants import STAT_EMOJI
from core.progression import exp_to_next
from typing import Dict

def exp_bar_emoji(player: Dict, length: int = 12) -> str:
    cur, nxt = player.get('exp', 0), exp_to_next(player.get('level', 1))
    filled = int((cur / nxt) * length) if nxt > 0 else 0
    return f"{'🟩'*filled}{'⬜'*(length-filled)} {cur}/{nxt} EXP"

def daily_progress_bar_emoji(player: Dict) -> str:
    keys = ['financial','mental','physical','personal']
    return ''.join('✅' if player.get('daily', {}).get(k) else '▫️' for k in keys)

def format_stats(player: Dict) -> str:
    return '\n'.join(f"{STAT_EMOJI.get(k,'')} {k.capitalize()}: {v}" for k, v in player.get('stats', {}).items())

def short_action_button_text(name: str, info: Dict) -> str:
    stat = info.get('stat')
    emoji = STAT_EMOJI.get(stat, "")
    cd = info.get('cooldown', 0)
    cd_text = ""
    if cd:
        if cd >= 86400:
            cd_text = f"·{cd//86400}d"
        elif cd >= 3600:
            cd_text = f"·{cd//3600}h"
        else:
            cd_text = f"·{cd//60}m"
    return f"{emoji} {name} {cd_text}"
