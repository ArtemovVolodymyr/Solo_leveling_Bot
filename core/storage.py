# core/storage.py
import json
import os
from typing import Dict, Any
from config.settings import PLAYERS_FILE
from data.constants import DEFAULT_STATS

def load_players() -> Dict[str, Any]:
    if not os.path.exists(PLAYERS_FILE):
        save_players({})
        return {}
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_players(data: Dict[str, Any]):
    os.makedirs(os.path.dirname(PLAYERS_FILE) or ".", exist_ok=True)
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def ensure_player_structure(player: Dict[str, Any]) -> Dict[str, Any]:
    player.setdefault("name", "Unknown")
    player.setdefault("level", 1)
    player.setdefault("exp", 0)
    player.setdefault("stats", DEFAULT_STATS.copy())
    player.setdefault("daily", {k: False for k in ['financial','mental','physical','personal']})
    player.setdefault("last_done", {})         # action -> iso timestamp
    player.setdefault("action_history", [])    # list of {"action":..., "ts":...}
    player.setdefault("achievements", [])
    player.setdefault("done_actions", [])
    return player

def get_player(user) -> Dict[str, Any]:
    players = load_players()
    uid = str(user.id)
    if uid not in players:
        name = (user.first_name or "") + ((" " + user.last_name) if user.last_name else "")
        players[uid] = {
            "name": name or f"User {uid}",
            "level":1, "exp":0, "stats": DEFAULT_STATS.copy(),
            "daily": {k: False for k in ['financial','mental','physical','personal']},
            "last_done": {}, "action_history": [], "achievements": [], "done_actions": []
        }
        save_players(players)
    player = players[uid]
    ensure_player_structure(player)
    return player

def save_player_for_user(user_id: int, player_data: Dict[str, Any]):
    players = load_players()
    players[str(user_id)] = player_data
    save_players(players)
