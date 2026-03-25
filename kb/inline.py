from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_days_kb():
    days = [
        ("Пн", "day_0"), ("Вт", "day_1"), ("Ср", "day_2"),
        ("Чт", "day_3"), ("Пт", "day_4"), ("Сб", "day_5")
    ]
    keyboard = [
        [InlineKeyboardButton(text, callback_data=data) for text, data in days[i:i+3]]
        for i in range(0, 6, 3)
    ]
    # Кнопку "Назад" удалили отсюда
    return InlineKeyboardMarkup(keyboard)

def get_groups_kb(groups: list):
    """Создает клавиатуру со списком групп"""
    keyboard = []
    # Делаем по 2 группы в ряд
    for i in range(0, len(groups), 2):
        row = [InlineKeyboardButton(groups[i], callback_data=f"setgroup_{groups[i]}")]
        if i + 1 < len(groups):
            row.append(InlineKeyboardButton(groups[i+1], callback_data=f"setgroup_{groups[i+1]}"))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)

def get_profile_kb():
    keyboard = [
        [InlineKeyboardButton("⚙️ Изменить группу", callback_data="change_group")],
        [InlineKeyboardButton("✍️ Написать в поддержку", url="https://t.me/твой_ник_админа")]
    ]
    return InlineKeyboardMarkup(keyboard)


