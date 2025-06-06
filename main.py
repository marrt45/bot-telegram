from telegram.ext import Application, MessageHandler, filters
from config import TELEGRAM_TOKEN
from gpt_manager import ConversationManager
from sheets import get_products_list
import logging

# Configura logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inicializa el administrador de conversación
conv_manager = ConversationManager()

async def handle_message(update, context):
    try:
        user_msg = update.message.text
        user = update.effective_user
        
        # Obtiene productos disponibles
        products_data = get_products_list()
        
        # Genera respuesta
        bot_reply = conv_manager.get_response(user_msg, products_data)
        
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Disculpe, ocurrió un error. Intente nuevamente.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Maneja todos los mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logging.info("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == '__main__':
    main()