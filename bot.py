import asyncio
import logging
from loader import dp, bot
from core.daily_reset import start_daily_reset_task

# Импорт хэндлеров (регистрируются автоматически)
import handlers.start_menu
import handlers.stats_handlers
import handlers.actions_handlers
import handlers.daily_handlers
import handlers.export_import_handlers
import handlers.extra_handlers

logging.basicConfig(level=logging.INFO)

async def main():
    # Запуск таска сброса дневных побед
    asyncio.create_task(start_daily_reset_task(bot))
    logging.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
