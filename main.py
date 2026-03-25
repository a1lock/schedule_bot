from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import settings
from handlers.base import start_command
from handlers.menu import handle_main_menu, handle_callbacks

def main():
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    # 1. Стартовая команда
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. Обработка текстовых кнопок (Главное меню)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))
    
    # 3. Обработка нажатий на inline-кнопки
    application.add_handler(CallbackQueryHandler(handle_callbacks))
    
    application.run_polling()

if __name__ == "__main__":
    main()