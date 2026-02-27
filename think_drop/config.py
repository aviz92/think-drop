import os
from dotenv import load_dotenv

from think_drop.llms.const import LLMType

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DB_ID")
LLM_PROVIDER = os.getenv("LLM_PROVIDER")  # options: "gemini", "claude", "gpt"

if LLM_PROVIDER == LLMType.GEMINI:
    LLM_API_KEY = os.getenv("GEMINI_API_KEY")
elif LLM_PROVIDER == LLMType.GPT:
    LLM_API_KEY = os.getenv("OPENAI_API_KEY")
elif LLM_PROVIDER == "claude":
    LLM_API_KEY = os.getenv("CLAUDE_API_KEY")
else:
    raise NotImplementedError(
        f"LLM provider '{LLM_PROVIDER}' is not supported. Choose from: {LLMType.GEMINI}, {LLMType.GPT}, 'claude'")

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
