# data/actions.py
# central place to add / modify actions and cooldowns (seconds)
ACTIONS = {
    "Slovak: lesson 1h": {"stat": "intelligence", "stat_gain": 1, "exp": 20, "category": "intellectual", "cooldown": 86400},
    "Slovak: 20 words": {"stat": "intelligence", "stat_gain": 0, "exp": 10, "category": "intellectual", "cooldown": 3600},
    "Slovak: grammar practice": {"stat": "intelligence", "stat_gain": 1, "exp": 15, "category": "intellectual", "cooldown": 86400},
    "English: lesson 1h": {"stat": "intelligence", "stat_gain": 1, "exp": 20, "category": "intellectual", "cooldown": 86400},
    "English: 20 words": {"stat": "intelligence", "stat_gain": 0, "exp": 10, "category": "intellectual", "cooldown": 3600},
    "Training 1h": {"stat": "strength", "stat_gain": 1, "exp": 15, "category": "physical", "cooldown": 86400},
    "Walk 30min": {"stat": "vitality", "stat_gain": 1, "exp": 5, "category": "physical", "cooldown": 3600},
    "Push-ups set": {"stat": "agility", "stat_gain": 0, "exp": 5, "category": "physical", "cooldown": 3600},
    "Work on income": {"stat": "finance", "stat_gain": 1, "exp": 15, "category": "financial", "cooldown": 86400},
    "Financial win": {"stat": "finance", "stat_gain": 2, "exp": 30, "category": "financial", "cooldown": 86400*7},
    "Coding practice 1h": {"stat": "intelligence", "stat_gain": 1, "exp": 20, "category": "intellectual", "cooldown": 86400},
    "Post / story": {"stat": "charisma", "stat_gain": 1, "exp": 10, "category": "personal", "cooldown": 3600},
    "Content plan": {"stat": "charisma", "stat_gain": 1, "exp": 15, "category": "personal", "cooldown": 86400},
    "Meditation 20min": {"stat": "discipline", "stat_gain": 1, "exp": 10, "category": "personal", "cooldown": 3600},
    "Focus 1h (no social)": {"stat": "discipline", "stat_gain": 1, "exp": 10, "category": "personal", "cooldown": 86400}
}
