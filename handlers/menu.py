from telegram import Update
from telegram.ext import ContextTypes
from services.time_utils import get_now, get_week_parity, get_russian_day
from services.schedule_service import get_schedule_for_day, format_schedule
from kb.inline import get_days_kb, get_week_kb, get_profile_kb
from datetime import timedelta

DEFAULT_GROUP = "ИПГС 1к 1 bo 08.03.01_ПГС"

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = get_now()
    
    if text == "📅 Сегодня":
        await _send_schedule_logic(update, now)
    elif text == "📆 Завтра":
        await _send_schedule_logic(update, now + timedelta(days=1))
    elif text == "🗓 По дням":
        await update.message.reply_text("🗓 *Выберите день недели:*", reply_markup=get_days_kb(), parse_mode="Markdown")
    elif text == "👤 Профиль":
        await update.message.reply_text("👤 *Твой профиль:*", reply_markup=get_profile_kb(), parse_mode="Markdown")

async def _send_schedule_logic(update: Update, target_dt):
    """Единая логика для отправки расписания (и для сообщений, и для колбэков)"""
    day_idx = target_dt.weekday()
    
    if day_idx == 6:
        msg = "Воскресенье — выходной! 🥳"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return

    parity = get_week_parity(target_dt.date())
    lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, parity)
    
    parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
    response = format_schedule(lessons, get_russian_day(day_idx), parity_text, target_dt)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(response, parse_mode="Markdown", reply_markup=get_days_kb())
    else:
        await update.message.reply_text(response, parse_mode="Markdown")

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        # Кнопка НАЗАД: редактируем сообщение обратно в выбор дней
        await query.edit_message_text(
            "🏠 Вы вернулись в меню выбора. Выберите день недели:",
            reply_markup=get_days_kb()
        )
    
    elif query.data.startswith("day_"):
        day_idx = int(query.data.split("_")[1])
        now = get_now()
        # Считаем дату выбранного дня относительно текущей недели
        target_dt = now + timedelta(days=(day_idx - now.weekday()))
        await _send_schedule_logic(update, target_dt)