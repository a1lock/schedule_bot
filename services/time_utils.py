from datetime import datetime, date
import pytz

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

def get_now() -> datetime:
    return datetime.now(MOSCOW_TZ)

def get_week_parity(target_date: date = None) -> str:
    if target_date is None:
        target_date = get_now().date()
    week_number = target_date.isocalendar()[1]
    return "odd" if week_number % 2 != 0 else "even"

def get_russian_day(day_idx: int) -> str:
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[day_idx]
