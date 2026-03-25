from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_days_kb():
    days = [
        ("Пн", "day_0"), ("Вт", "day_1"), ("Ср", "day_2"),
        ("Чт", "day_3"), ("Пт", "day_4"), ("Сб", "day_5")
    ]
    # Делаем сетку 3х2
    keyboard = [
        [InlineKeyboardButton(text, callback_data=data) for text, data in days[i:i+3]]
        for i in range(0, 6, 3)
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_week_kb():
    keyboard = [
        [InlineKeyboardButton("Эта неделя", callback_data="week_current")],
        [InlineKeyboardButton("Следующая неделя", callback_data="week_next")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_profile_kb():
    keyboard = [
        [InlineKeyboardButton("✍️ Написать в поддержку", callback_data="support")],
        [InlineKeyboardButton("⚙️ Изменить параметры (Очная/Заочная)", callback_data="toggle_form")],
        [InlineKeyboardButton("🎓 Уровень образования", callback_data="edu_level")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)