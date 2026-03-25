import pdfplumber
import pandas as pd
import re
from database.models import LessonParity

class ScheduleParser:
    def __init__(self):
        # Соответствие дней недели
        self.days_map = {
            "ПОНЕДЕЛЬНИК": 0, "ВТОРНИК": 1, "СРЕДА": 2,
            "ЧЕТВЕРГ": 3, "ПЯТНИЦА": 4, "СУББОТА": 5
        }

    def parse_file(self, file_path):
        results = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Извлекаем таблицу
                table = page.extract_table({
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                })
                
                if not table: continue
                
                df = pd.DataFrame(table)
                
                # 1. Определяем группы (они в первой значимой строке)
                # Обычно это 0-я или 1-я строка
                groups = df.iloc[0, 3:].values 
                
                current_day = 0
                
                for row_idx in range(1, len(df)):
                    row = df.iloc[row_idx]
                    
                    # Определяем день недели
                    day_cell = str(row[0]).strip().replace('\n', '')
                    if day_cell in self.days_map:
                        current_day = self.days_map[day_cell]
                    
                    # Номер пары
                    try:
                        lesson_num = int(str(row[2]).strip())
                    except:
                        continue

                    # Проходим по каждой группе (колонке)
                    for col_idx, group_name in enumerate(groups):
                        if not group_name: continue
                        
                        cell_text = row[col_idx + 3]
                        if not cell_text or len(cell_text.strip()) < 5:
                            continue

                        # ЛОГИКА ВЕРХ / НИЗ
                        # Если в ячейке есть перенос строки, который делит её 
                        # на две части (визуально как в PDF), обрабатываем обе
                        parts = [p.strip() for p in cell_text.split('\n\n') if len(p.strip()) > 5]
                        
                        if len(parts) == 2:
                            # Верхняя часть - нечетная, нижняя - четная
                            results.append(self._create_entry(group_name, current_day, lesson_num, parts[0], LessonParity.ODD))
                            results.append(self._create_entry(group_name, current_day, lesson_num, parts[1], LessonParity.EVEN))
                        else:
                            # Одна пара на всю ячейку
                            results.append(self._create_entry(group_name, current_day, lesson_num, cell_text, LessonParity.ALWAYS))
                            
        return results

    def _create_entry(self, group, day, num, text, parity):
        # Чистим текст от лишних переносов
        clean_text = " ".join(text.split())
        return {
            "group_name": group,
            "day": day,
            "num": num,
            "text": clean_text,
            "parity": parity
        }