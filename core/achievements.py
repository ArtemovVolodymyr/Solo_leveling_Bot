# core/achievements.py
from typing import List, Dict

def check_achievements(player: Dict) -> List[str]:
    messages = []
    player.setdefault("achievements", [])
    if player.get('level', 0) >= 2 and 'first_level' not in player['achievements']:
        player['achievements'].append('first_level')
        messages.append("🏆 Достижение: Первый уровень!")
    if len(player.get('action_history', [])) >= 10 and '10_actions' not in player['achievements']:
        player['achievements'].append('10_actions')
        messages.append("🏆 Достижение: 10 выполненных действий!")
    return messages
