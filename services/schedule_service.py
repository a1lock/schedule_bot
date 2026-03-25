from sqlalchemy import select
from database.core import async_session
from database.models import Lesson, LessonParity
from datetime import datetime

# Время начала каждой пары
LESSON_TIME = {
    1: "08:30 - 09:50",
    2: "10:00 - 11:20",
    3: "11:30 - 12:50",
    4: "13:00 - 14:20",
    5: "14:30 - 15:50",
    6: "16:00 - 17:20"
}

async def get_schedule_for_day(group_name: str, day_idx: int, parity: str):
    async with async_session() as session:
        # Ищем пары для конкретной группы, дня и учитываем четность
        # Выбираем пары, где parity совпадает ИЛИ стоит ALWAYS
        query = select(Lesson).where(
            Lesson.group_name == group_name,
            Lesson.day_of_week == day_idx,
            (Lesson.parity == parity) | (Lesson.parity == LessonParity.ALWAYS)
        ).order_by(Lesson.lesson_number)
        
        result = await session.execute(query)
        lessons = result.scalars().all()
        return lessons

def format_schedule(lessons, day_name: str, parity_name: str) -> str:
    # Добавим дату для наглядности
    current_date = datetime.now().strftime("%d.%m")
    
    header = f"📅 *{day_name}* ({current_date})\n"
    header += f"🔢 *{parity_name}*\n"
    header += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
    
    if not lessons:
        return header + "Пар нет! Можно отдыхать. 😎"
    
    text = header
    for l in lessons:
        time = LESSON_TIME.get(l.lesson_number, "")
        # Выбираем эмодзи по типу занятия
        icon = "📘" if "л." in (l.lesson_type or "") else "📗" if "пр." in (l.lesson_type or "") else "📙"
        
        text += f"*{l.lesson_number} пара* | {time}\n"
        text += f"{icon} {l.subject}\n"
        if l.teacher:
            text += f"└ 👨‍🏫 {l.teacher}\n"
        if l.room:
            text += f"└ 🚪 {l.room}\n"
        text += "\n"
    
    return text
