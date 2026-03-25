FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Не пишем .pyc файлы на диск и не буферизуем stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Запускаем бота
CMD ["python", "main.py"]