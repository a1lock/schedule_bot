from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    keyboard = [
        [KeyboardButton("📅 Сегодня"), KeyboardButton("📆 Завтра")],
        [KeyboardButton("🗓 По дням"), KeyboardButton("⏳ На неделю")],
        [KeyboardButton("👤 Профиль")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Выберите раздел...")