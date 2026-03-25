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

# Оставим ее только для профиля, если там будет вложенность
def get_profile_kb():
    keyboard = [
        [InlineKeyboardButton("✍️ Написать в поддержку", callback_data="support")],
        [InlineKeyboardButton("🎓 Уровень образования", callback_data="edu_level")]
    ]
    return InlineKeyboardMarkup(keyboard)