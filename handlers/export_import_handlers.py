# handlers/export_import_handlers.py
import json, os
from aiogram import types
from aiogram.types import InputFile
from loader import dp
from core.storage import get_player, save_player_for_user, load_players

@dp.message_handler(lambda m: m.text == '💾 Экспорт')
async def menu_export(message: types.Message):
    player = get_player(message.from_user)
    filename = f"player_{message.from_user.id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(player, f, ensure_ascii=False, indent=4)
    await message.reply_document(InputFile(filename))
    os.remove(filename)

@dp.message_handler(lambda m: m.text == '📂 Импорт')
async def menu_import(message: types.Message):
    await message.reply("Пришлите JSON-файл с профилем (как был получен через Экспорт).")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_import_document(message: types.Message):
    if message.document and message.document.file_name.endswith(".json"):
        file = await message.document.download(destination_dir=".")
        try:
            with open(file.name, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON structure")
            save_player_for_user(message.from_user.id, data)
            await message.reply("Профиль успешно импортирован.")
        except Exception as e:
            await message.reply(f"Ошибка при импорте: {e}")
        finally:
            try:
                os.remove(file.name)
            except Exception:
                pass
    else:
        await message.reply("Пожалуйста, пришлите JSON-файл.")
