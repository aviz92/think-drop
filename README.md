[![Python](https://img.shields.io/badge/python-%3E=3.12-blue)](https://www.python.org/)
[![Development Status](https://img.shields.io/badge/status-stable-green)](https://github.com/aviz92/think-drop)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)](https://github.com/aviz92/think-drop)
[![License](https://img.shields.io/github/license/aviz92/think-drop)](LICENSE)

---

# 💡 Think-Drop
A personal Telegram bot that captures your text and voice notes, classifies them by category, and writes clean summaries directly to your Notion workspace — powered by AI.

---

## 📦 Installation
```bash
git clone https://github.com/aviz92/think-drop.git
cd think-drop
uv sync
```

---

## 🚀 Features
  - **Auto-classification** — Gemini automatically classifies your note into the right category (Work, Home, Ideas, Shopping, Meetings, Reading, Decisions, Personal)
  - **Smart summarization** — every note gets a clean title and concise summary before being saved
  - **Notion integration** — notes are written directly to your Notion database with full metadata (category, source, date, raw text)
  - **Generic LLM layer** — swap Gemini for Claude or OpenAI by changing a single line in `llm.py`
  - **Voice support** — coming in phase 2

---

## ⚙️ Configuration

Create a `.env` file with the following variables:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NOTION_TOKEN=your_notion_internal_integration_secret
NOTION_DB_ID=your_notion_database_id
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🛠️ How to Use

### 🤖 Creating a Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather). 
2. Send the command /newbot. 
3. Follow the prompts to name your bot and choose a username. 
4. In the end, you'll get a Bot Token – save it, you'll need it in the .env file.


### 🧠 LLM API Key
- Get your Gemini API key from your provider (e.g., Google - Gemini, OpenAI - GPT-x, Anthropic - Claude, etc).
- In this project we use Gemini API, you can get your API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)


### 🧩 Setting Up Notion Integration
1. Generated Internal Integration Token
    - Go your Notion internal integration secret at [notion.so/my-integrations](https://www.notion.so/profile/integrations/internal). 
    - Click + New integration. 
    - Give it a name and select the workspace. 
    - Save the generated Internal Integration Token. 
2. Create a new database in Notion with the following properties:
   - Title (title)
   - Summary (text)
   - Raw (text)
   - Category (select)
   - Source (name)
   - Date (date)
3. Connect your integration to the database by sharing the database with your integration's email (found in the integration settings)
4. Get your Notion database id <br>
   - Open your **Notion database as a full page** (the URL of the page containing your database). It's the ID of the embedded database itself
   - The ID is the section before the `?v=` in the URL - `notion.so/<Your-Database-ID>?v=<Page-ID>`
     - Alternatively, if your database is embedded inside a page, the page URL ID and the database ID are different — use the Notion API or inspect the page to find the real database ID.

---

## 🚀 Quick Start
```bash
uv run main.py
```

Then open Telegram, find your bot and send `/start`.

---

## 🤝 Contributing

If you have a helpful pattern or improvement to suggest:
Fork the repo
Create a new branch
Submit a pull request
I welcome additions that promote clean, productive, and maintainable development.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Thanks

Thanks for exploring this repository!
Happy coding!
