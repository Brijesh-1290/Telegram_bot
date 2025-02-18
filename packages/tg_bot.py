import time

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from packages.ai_chatbot import chatbot
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. How can I help you today?')


def echo(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    msg = update.message.text
    try:
        response = chatbot(msg)
    except Exception as e:
        response = "Some unexpected error occurred! please wait for 1 min."
        try:
            time.sleep(60)
            response = chatbot(msg)
        except Exception as e:
            print(str(e))
    update.message.reply_text(response)
    print(f"{username}: {msg}")
    print(f"Bot: {response}")


def main() -> None:
    PORT = int(os.environ.get('PORT', 8443))
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # updater.start_polling()
    # Add a webhook to bind to the port
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN)
    updater.bot.set_webhook(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{BOT_TOKEN}")
    updater.idle()


if __name__ == '__main__':
    main()
