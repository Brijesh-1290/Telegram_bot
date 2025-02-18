from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from open_ai import chatbot
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. How can I help you today?')


def echo(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    msg = update.message.text
    response = chatbot(msg)
    update.message.reply_text(response)
    print(f"{username}: {msg}")
    print(f"Bot: {response}")


def main() -> None:
    bot_token = os.getenv('BOT_TOKEN')
    print(1)
    print(bot_token)
    print(1)
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
