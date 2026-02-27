import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DB_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CATEGORIES = [
    "Work",
    "Home",
    "Ideas",
    "Shopping",
    "Meetings",
    "Reading",
    "Decisions",
    "Personal",
]
