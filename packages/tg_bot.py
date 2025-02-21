import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from packages.ai_chatbot import chatbot
from dotenv import load_dotenv
import os
from packages.db import conversations

# Load environment variables from a .env file
load_dotenv()
SYSTEM_CONTENT = os.getenv('SYSTEM_CONTENT')


def get_chat(identifier):
    chat = [
        {"role": "system",
         "content": SYSTEM_CONTENT}
    ]
    # Fetch user's conversation history
    user_conversations = conversations.find({"identifier": identifier})
    for convo in user_conversations:
        chat.extend(
            [{"role": "user", "content": convo['message']}, {"role": "assistant", "content": convo['response']}])
    return chat


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. How can I help you today?')


def echo(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    identifier = user.username if user.username else user.name
    chat = get_chat(identifier)
    msg = update.message.text
    try:
        chat.append({"role": "user", "content": msg})
        response = chatbot(chat)
        chat.append({"role": "assistant", "content": response})
    except Exception as e:
        response = "Some unexpected error occurred! please try again after some time."

    update.message.reply_text(response)

    # Store conversation in MongoDB
    conversation = {
        "identifier": identifier,
        "message": msg,
        "response": response,
        "timestamp": update.message.date
    }
    conversations.insert_one(conversation)

    print(f"{identifier}: {msg}")
    print(f"Bot: {response}")


def clear(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    identifier = user.username if user.username else user.name
    conversations.delete_many({"identifier": identifier})
    update.message.reply_text('Your conversation history has been cleared.')


def main() -> None:
    PORT = int(os.environ.get('PORT', 8443))
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(CommandHandler('clear', clear))

    updater.start_polling()
    # Add a webhook to bind to the port
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN)
    # updater.bot.set_webhook(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{BOT_TOKEN}")
    updater.idle()


if __name__ == '__main__':
    main()
