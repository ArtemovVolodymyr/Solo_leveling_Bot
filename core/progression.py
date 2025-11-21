# core/progression.py
from typing import List, Dict

def exp_to_next(level: int) -> int:
    # simple linear curve; change if needed
    return 100 * level

def add_exp(player: Dict, amount: int) -> List[str]:
    player['exp'] += amount
    messages = []
    while player['exp'] >= exp_to_next(player['level']):
        player['exp'] -= exp_to_next(player['level'])
        player['level'] += 1
        messages.append(f"🎉 LEVEL UP! Новый уровень: {player['level']}")
    return messages
