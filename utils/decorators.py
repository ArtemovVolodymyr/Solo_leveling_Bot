# utils/decorators.py
from functools import wraps
from aiogram import types
from config.settings import OWNER_ID

def owner_only(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, *args, **kwargs):
        if message.from_user.id != OWNER_ID:
            await message.reply("Только админ может использовать эту команду.")
            return
        return await handler(message, *args, **kwargs)
    return wrapper
