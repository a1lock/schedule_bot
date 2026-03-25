from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import settings
from handlers.base import start_command
from handlers.menu import handle_main_menu, handle_callbacks
from logger import logger

async def error_handler(update, context):
    logger.error(f"❌ Ошибка при обработке обновления {update}: {context.error}")

def main():
    logger.info("🚀 Запуск бота...")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    # Регистрация хендлеров
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))
    application.add_handler(CallbackQueryHandler(handle_callbacks))
    
    # Регистрация обработчика ошибок
    application.add_error_handler(error_handler)
    
    logger.info("📡 Бот начал опрос Telegram (Polling)...")
    application.run_polling()

if __name__ == "__main__":
    main()