# Solo-Leveling Telegram Bot (modular)
Structure:
- bot.py — entrypoint, creates Bot and Dispatcher
- config/ — settings
- data/ — actions, categories, constants
- core/ — storage, progression, visual, daily reset
- handlers/ — message/callback handlers
- keyboards/ — keyboard builders
- utils/ — helpers

To run:
1. pip install aiogram
2. export BOT_TOKEN or edit config/settings.py
3. python bot.py
