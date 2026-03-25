from telegram import Update
from telegram.ext import ContextTypes
from kb.reply import get_main_menu
from logger import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} ({user.first_name}) started the bot.")
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"Я — твой умный бот-расписание. Выбери нужный раздел в меню ниже:",
        reply_markup=get_main_menu()
    )