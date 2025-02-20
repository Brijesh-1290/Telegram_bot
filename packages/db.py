from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

connection_string = (f"mongodb+srv://{db_user}:{db_password}@cluster0.7xvss.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(connection_string)
db = client['TelegramBot']
conversations = db['chats']