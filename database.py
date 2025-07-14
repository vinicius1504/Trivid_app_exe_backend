import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("DATABASE_URL")

client = MongoClient(MONGO_URI)
db = client["Testo"]
usuarios_collection = db["User"]
