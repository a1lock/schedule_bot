from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from services.time_utils import get_week_parity, get_russian_day
from services.schedule_service import get_schedule_for_day, format_schedule
from kb.reply import get_main_menu
from kb.inline import get_days_kb, get_week_kb, get_profile_kb

# Тестовая группа (в реальном боте будем брать из БД профиля пользователя)
DEFAULT_GROUP = "ИПГС 1к 1 bo 08.03.01_ПГС"

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    today = datetime.now()
    parity = get_week_parity()
    
    if text == "📅 Сегодня":
        day_idx = today.weekday()
        # Если сегодня воскресенье (6) - сразу говорим, что пар нет
        if day_idx == 6:
            await update.message.reply_text("Сегодня воскресенье! Пар нет, отдыхай. 🥳")
            return

        lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, parity)
        
        # Меняем названия тут:
        parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
        
        response = format_schedule(lessons, get_russian_day(day_idx), parity_text)
        await update.message.reply_text(response, parse_mode="Markdown")
        
    elif text == "📆 Завтра":
        tomorrow = today + timedelta(days=1)
        day_idx = tomorrow.weekday()
        
        # Если завтра понедельник, четность недели меняется
        current_parity = parity
        if day_idx == 0:
            current_parity = "even" if parity == "odd" else "odd"
        
        if day_idx == 6:
            await update.message.reply_text("Завтра воскресенье! Можно выспаться. 😴")
            return

        lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, current_parity)
        
        # И тут:
        parity_text = "Нечетная неделя" if current_parity == "odd" else "Четная неделя"
        
        response = format_schedule(lessons, get_russian_day(day_idx), parity_text)
        await update.message.reply_text(response, parse_mode="Markdown")

        
    elif text == "🗓 По дням":
        await update.message.reply_text("Выберите день недели:", reply_markup=get_days_kb())
        
    elif text == "⏳ На неделю":
        await update.message.reply_text("Выберите неделю:", reply_markup=get_week_kb())
        
    elif text == "👤 Профиль":
        await update.message.reply_text("⚙️ Настройки профиля:", reply_markup=get_profile_kb())

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на Inline-кнопки"""
    query = update.callback_query
    await query.answer() # Обязательно подтверждаем нажатие
    
    if query.data == "main_menu":
        await query.edit_message_text("Вы вернулись в главное меню. Используйте кнопки внизу.")
    
    elif query.data.startswith("day_"):
        day_idx = query.data.split("_")[1]
        await query.edit_message_text(f"Расписание на выбранный день (ID: {day_idx}) скоро будет тут!")
        
    # Остальные callback_data обработаем позже