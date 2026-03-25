from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from services.time_utils import get_now, get_week_parity, get_russian_day
from services.schedule_service import get_schedule_for_day, format_schedule
from kb.inline import get_days_kb, get_profile_kb
from datetime import timedelta
from logger import logger

DEFAULT_GROUP = "ИПГС 1к 1 bo 08.03.01_ПГС"

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = get_now()
    
    if text == "📅 Сегодня":
        await _send_schedule_logic(update, now)
    elif text == "📆 Завтра":
        await _send_schedule_logic(update, now + timedelta(days=1))
    elif text == "🗓 По дням":
        await update.message.reply_text(
            "🗓 <b>Выберите день недели:</b>", 
            reply_markup=get_days_kb(),
            parse_mode=ParseMode.HTML # Везде меняем на HTML
        )
    elif text == "👤 Профиль":
        await update.message.reply_text(
            "👤 <b>Твой профиль:</b>", 
            reply_markup=get_profile_kb(),
            parse_mode=ParseMode.HTML
        )

async def _send_schedule_logic(update: Update, target_dt):
    day_idx = target_dt.weekday()
    
    # Если это воскресенье
    if day_idx == 6:
        msg = "<b>Воскресенье — выходной!</b> 🥳"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_days_kb())
        else:
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        return

    parity = get_week_parity(target_dt.date())
    lessons = await get_schedule_for_day(DEFAULT_GROUP, day_idx, parity)
    
    parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
    response = format_schedule(lessons, get_russian_day(day_idx), parity_text, target_dt)
    
    if update.callback_query:
        # Редактируем сообщение при нажатии на кнопку дня
        await update.callback_query.edit_message_text(
            response, 
            parse_mode=ParseMode.HTML, 
            reply_markup=get_days_kb()
        )
    else:
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    logger.info(f"==== CALLBACK RECEIVED: {query.data} ====")
    await query.answer()
    
    logger.info(f"Нажата кнопка: {query.data}") # Проверим в логах
    
    if query.data == "main_menu":
        await query.edit_message_text(
            "🏠 <b>Меню выбора дня:</b>",
            reply_markup=get_days_kb(),
            parse_mode="HTML" # Пишем строкой для надежности
        )
    
    elif query.data.startswith("day_"):
        day_idx = int(query.data.split("_")[1])
        now = get_now()
        target_dt = now + timedelta(days=(day_idx - now.weekday()))
        await _send_schedule_logic(update, target_dt)
