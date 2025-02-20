import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from packages.ai_chatbot import chatbot
from dotenv import load_dotenv
import os
from packages.db import conversations

# Load environment variables from a .env file
load_dotenv()

chat = [
    {"role": "system",
     "content": "You are a helpful assistant created by Brijesh K Babu. So if anyone ask about your creator, tell them it's Brijesh K Babu. This is the summary about Brijesh : Dedicated and results-driven Python Developer with 1.5 years of experience in developing and maintaining software tools for testing electronic boards. Proficient in Python, Django, FastAPI, Flask, and PyQt for creating intuitive user interfaces. Strong background in SQL and MongoDB for database management, and hands-on experience with JavaScript, React, TypeScript, Node.js, and Express.js for full-stack development. Experienced in unit testing and automated testing using pytest. Demonstrated growth through a successful internship leading to a permanent position. Built demo projects in Django and MERN stack. Developed a tool to manage and download electronic test scripts. Implemented a yield tracker functionality to improve productivity. Adept at problem-solving and delivering high-quality solutions in fast-paced environments."}
]


def start(update: Update, context: CallbackContext) -> None:
    global chat
    update.message.reply_text('Hello! I am your bot. How can I help you today?')
    user = update.message.from_user
    identifier = user.username if user.username else user.id

    # Fetch user's conversation history
    user_conversations = conversations.find({"identifier": identifier})
    for convo in user_conversations:
        chat.extend([{"role": "user", "content": convo['message']},{"role": "assistant", "content": convo['response']}])


def echo(update: Update, context: CallbackContext) -> None:
    global chat
    convo = chat
    user = update.message.from_user
    identifier = user.username if user.username else user.id
    msg = update.message.text
    try:
        convo.append({"role": "user", "content": msg})
        response = chatbot(convo)
        convo.append({"role": "assistant", "content": response})
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
    identifier = user.username if user.username else user.id
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
