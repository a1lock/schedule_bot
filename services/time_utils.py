from datetime import datetime, date

def get_week_parity() -> str:
    """Возвращает 'odd' для нечетных недель и 'even' для четных."""
    # Узнаем номер недели в году
    week_number = date.today().isocalendar()[1]
    # Если номер недели нечетный - это числитель, четный - знаменатель
    return "odd" if week_number % 2 != 0 else "even"

def get_russian_day(day_idx: int) -> str:
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[day_idx]