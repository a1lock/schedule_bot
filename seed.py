import asyncio
import os
import re
from sqlalchemy import select
from database.core import async_session
from database.models import Lesson, LessonParity
from services.pdf_parser import ScheduleParser

# --- ФУНКЦИЯ РАЗБОРА ТЕКСТА (теперь она прямо здесь) ---
def parse_lesson_text(text: str):
    # Очистка текста от лишних пробелов
    text = " ".join(text.split())
    
    # Ищем тип (л.|пр.|лаб.|КОП|КРП)
    lesson_type_match = re.match(r"^(л\.|пр\.|лаб\.|КОП|КРП)\s*", text, re.IGNORECASE)
    lesson_type = lesson_type_match.group(1) if lesson_type_match else None
    remaining = re.sub(r"^(л\.|пр\.|лаб\.|КОП|КРП)\s*", "", text, flags=re.IGNORECASE)

    # Ищем маску недель (например, 2,6,10,14 нед.)
    week_mask = None
    week_match = re.search(r"(\d+(?:,\d+)*)\s*нед\.", remaining)
    if week_match:
        week_mask = week_match.group(1)
        remaining = remaining.replace(week_match.group(0), "").strip()

    # Делим на Предмет и всё остальное (ищем должность препода)
    parts = re.split(r"(доц\.|ст\.пр\.|проф\.|пр\.)", remaining, maxsplit=1)
    subject = parts[0].strip()
    
    teacher_and_room = "".join(parts[1:]) if len(parts) > 1 else ""
    # Ищем номер кабинета (цифры в конце, иногда через слеш)
    room_match = re.search(r"(\d+\s*/?\s*[А-Я-]+)$", teacher_and_room)
    room = room_match.group(1) if room_match else None
    teacher = teacher_and_room.replace(room, "").strip() if room else teacher_and_room

    return subject, lesson_type, teacher, room, week_mask

# --- ОСНОВНАЯ ЛОГИКА ЗАПОЛНЕНИЯ ---
async def auto_seed():
    parser = ScheduleParser()
    
    # Путь к папке с PDF внутри контейнера
    folder_path = "schedules"
    
    # Получаем список всех pdf файлов в папке
    if not os.path.exists(folder_path):
        print(f"❌ Папка {folder_path} не найдена!")
        return

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    if not files:
        print(f"❌ В папке {folder_path} нет PDF файлов!")
        return

    async with async_session() as session:
        total_count = 0
        for f in files:
            print(f"📦 Парсим {f}...")
            try:
                lessons_data = parser.parse_file(f)
                for entry in lessons_data:
                    subj, l_type, teach, room, mask = parse_lesson_text(entry["text"])
                    
                    lesson = Lesson(
                        group_name=entry["group_name"],
                        day_of_week=entry["day"],
                        lesson_number=entry["num"],
                        subject=subj,
                        lesson_type=l_type,
                        teacher=teach,
                        room=room,
                        parity=entry["parity"],
                        week_mask=mask
                    )
                    session.add(lesson)
                    total_count += 1
            except Exception as e:
                print(f"⚠️ Ошибка при парсинге {f}: {e}")

        await session.commit()
        print(f"🚀 ПОБЕДА! Автоматически загружено {total_count} пар.")

if __name__ == "__main__":
    asyncio.run(auto_seed())