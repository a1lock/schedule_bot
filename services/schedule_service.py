from datetime import datetime
from sqlalchemy import select
from database.core import async_session
from database.models import Lesson, LessonParity
import html

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

def format_schedule(lessons, day_name: str, parity_name: str, target_date: datetime) -> str:
    date_str = target_date.strftime("%d.%m")
    
    # Заголовок с использованием HTML тегов <b> и <i>
    header = f"📅 <b>{day_name} ({date_str})</b>\n"
    header += f"🔢 <b>{parity_name}</b>\n"
    header += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
    
    if not lessons:
        return header + "Пар нет! Можно отдыхать. 😎"
    
    text = header
    for l in lessons:
        time = LESSON_TIME.get(l.lesson_number, "??:??")
        icon = "📘" if "л." in (l.lesson_type or "") else "📗" if "пр." in (l.lesson_type or "") else "📙"
        
        # Экранируем данные из БД, чтобы символы <, > или & не сломали HTML
        subj = html.escape(l.subject)
        teacher = html.escape(l.teacher or "---")
        room = html.escape(l.room or "---")
        
        text += f"<b>{l.lesson_number} пара</b> | {time}\n"
        text += f"{icon} {subj}\n"
        text += f"└ 👨‍🏫 {teacher}\n"
        text += f"└ 🚪 {room}\n\n"
    
    return text

