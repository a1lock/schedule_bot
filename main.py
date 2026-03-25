from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import settings
from handlers.base import start_command
from handlers.menu import handle_main_menu, handle_callbacks
from logger import logger

async def error_handler(update, context):
    """Логируем ошибки, которые дошли до библиотеки"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    logger.info("Starting bot application...")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    # Регистрация хендлеров
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))
    application.add_handler(CallbackQueryHandler(handle_callbacks))
    
    # Добавляем логгер ошибок
    application.add_error_handler(error_handler)
    
    logger.info("Bot is polling...")
    # Убрали проблемный allowed_updates
    application.run_polling()

if __name__ == "__main__":
    main()