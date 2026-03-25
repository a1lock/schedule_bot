from telegram import Update
from telegram.ext import ContextTypes
from services.time_utils import get_now, get_week_parity, get_russian_day
from services.schedule_service import get_schedule_for_day, format_schedule
from kb.inline import get_days_kb, get_week_kb, get_profile_kb
import datetime

DEFAULT_GROUP = "ИПГС 1к 1 bo 08.03.01_ПГС"

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = get_now()
    
    if text == "📅 Сегодня":
        await _send_day_schedule(update, now.date())
        
    elif text == "📆 Завтра":
        await _send_day_schedule(update, now.date() + datetime.timedelta(days=1))
        
    elif text == "🗓 По дням":
        await update.message.reply_text("Выберите день недели:", reply_markup=get_days_kb())

    elif text == "⏳ На неделю":
        await update.message.reply_text("Выберите неделю:", reply_markup=get_week_kb())
        
    elif text == "👤 Профиль":
        await update.message.reply_text("⚙️ Настройки профиля:", reply_markup=get_profile_kb())

async def _send_day_schedule(update: Update, target_date: datetime.date):
    day_idx = target_date.weekday()
    if day_idx == 6:
        await update.message.reply_text("Воскресенье — выходной! 🥳")
        return

    parity = get_week_parity(target_date)
    lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, parity)
    
    parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
    response = format_schedule(lessons, get_russian_day(day_idx), parity_text, target_date)
    await update.message.reply_text(response, parse_mode="Markdown")

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        # Вместо просто текста, даем понять, что мы вернулись
        await query.edit_message_text("🏠 Вы в главном меню. Выберите нужный раздел на кнопках внизу.")
    
    elif query.data.startswith("day_"):
        day_idx = int(query.data.split("_")[1])
        # Для выбора по дням используем текущую четность недели
        parity = get_week_parity()
        lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, parity)
        
        parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
        response = format_schedule(lessons, get_russian_day(day_idx), parity_text, get_now().date())
        
        # Редактируем старое сообщение, добавляя расписание и кнопку назад
        await query.edit_message_text(response, parse_mode="Markdown", reply_markup=get_days_kb())