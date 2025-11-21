# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton('📊 Статы'),
        KeyboardButton('🎯 Действия'),
        KeyboardButton('📈 Уровень'),
        KeyboardButton('✅ Дневные победы'),
        KeyboardButton('💾 Экспорт'),
        KeyboardButton('📂 Импорт'),
        KeyboardButton('🏆 Достижения'),
        KeyboardButton('🕒 История 7д')
    )
    return kb
