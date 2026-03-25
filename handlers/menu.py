from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from services.time_utils import get_now, get_week_parity, get_russian_day
from services.schedule_service import get_schedule_for_day, format_schedule
from kb.inline import get_days_kb, get_profile_kb, get_groups_kb
from services.user_service import get_user_profile, get_all_groups, create_or_update_user
from datetime import timedelta
from logger import logger

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # 1. Получаем профиль пользователя
    profile = await get_user_profile(user_id)
    now = get_now()

    # 2. Если профиля нет и это не кнопка "Профиль", просим выбрать группу
    if not profile and text != "👤 Профиль":
        groups = await get_all_groups()
        await update.message.reply_text(
            "Привет! Я еще не знаю твою группу. Пожалуйста, выбери её из списка ниже:",
            reply_markup=get_groups_kb(groups)
        )
        return

    # 3. Логика кнопок
    if text == "📅 Сегодня":
        await _send_schedule_logic(update, now, profile.group_name)
        
    elif text == "📆 Завтра":
        await _send_schedule_logic(update, now + timedelta(days=1), profile.group_name)
        
    elif text == "🗓 По дням":
        await update.message.reply_text(
            "🗓 <b>Выберите день недели:</b>", 
            reply_markup=get_days_kb(),
            parse_mode=ParseMode.HTML
        )
        
    elif text == "👤 Профиль":
        group_display = profile.group_name if profile else "Не выбрана"
        await update.message.reply_text(
            f"👤 <b>Твой профиль</b>\n\n"
            f"📍 Группа: <code>{group_display}</code>\n"
            f"🎓 Направление: ИПГС",
            reply_markup=get_profile_kb(),
            parse_mode=ParseMode.HTML
        )

async def _send_schedule_logic(update: Update, target_dt, group_name: str):
    """Универсальная функция отправки расписания"""
    day_idx = target_dt.weekday()
    
    # Обработка воскресенья
    if day_idx == 6:
        msg = "<b>Воскресенье — выходной!</b> 🥳"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        return

    # Получаем расписание
    parity = get_week_parity(target_dt.date())
    lessons = await get_schedule_for_day(group_name, day_idx, parity)
    
    parity_text = "Нечетная неделя" if parity == "odd" else "Четная неделя"
    response = format_schedule(lessons, get_russian_day(day_idx), parity_text, target_dt)
    
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                response, 
                parse_mode=ParseMode.HTML, 
                reply_markup=get_days_kb()
            )
        else:
            await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    except BadRequest as e:
        if "Message is not modified" not in str(e):
            raise e

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    profile = await get_user_profile(user.id)

    logger.info(f"🔘 Нажата кнопка: {query.data}")

    # Смена группы
    if query.data == "change_group":
        groups = await get_all_groups()
        await query.edit_message_text("Выберите вашу группу из списка:", reply_markup=get_groups_kb(groups))

    # Сохранение выбранной группы
    elif query.data.startswith("setgroup_"):
        group_name = query.data.replace("setgroup_", "")
        await create_or_update_user(user.id, user.username, group_name)
        await query.edit_message_text(
            f"✅ Группа <b>{group_name}</b> сохранена!\nТеперь ты можешь смотреть расписание.", 
            parse_mode=ParseMode.HTML
        )

    # Выбор конкретного дня
    elif query.data.startswith("day_"):
        if not profile:
            await query.edit_message_text("Сначала выберите группу в профиле!")
            return
            
        day_idx = int(query.data.split("_")[1])
        now = get_now()
        # Считаем дату этого дня на текущей неделе
        target_dt = now + timedelta(days=(day_idx - now.weekday()))
        await _send_schedule_logic(update, target_dt, profile.group_name)