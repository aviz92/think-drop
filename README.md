[![Python](https://img.shields.io/badge/python-%3E=3.12-blue)](https://www.python.org/)
[![Development Status](https://img.shields.io/badge/status-stable-green)](https://github.com/aviz92/think-drop)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)](https://github.com/aviz92/think-drop)
[![License](https://img.shields.io/github/license/aviz92/think-drop)](LICENSE)

---

# 🧠 Think-Drop

A personal Telegram bot that captures your text and voice notes, classifies them by category, and writes clean summaries directly to your Notion workspace — powered by AI.

---

## 📦 Installation
```bash
git clone https://github.com/aviz92/think-drop.git
cd think-drop
uv sync
```

---

## ⚙️ Configuration

Create a `.env` file with the following variables:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
NOTION_TOKEN=your_notion_internal_integration_secret
NOTION_DB_ID=your_notion_database_id
GEMINI_API_KEY=your_gemini_api_key
```

- Get your Telegram token from [@BotFather](https://t.me/BotFather)
- Get your Notion internal integration secret from [notion.so/my-integrations](https://www.notion.so/my-integrations)
- Get your Gemini API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

## 🚀 Quick Start
```bash
uv run main.py
```

Then open Telegram, find your bot and send `/start`.

---

## 🚀 Features

* **Auto-classification** — Gemini automatically classifies your note into the right category (Work, Home, Ideas, Shopping, Meetings, Reading, Decisions, Personal)
* **Smart summarization** — every note gets a clean title and concise summary before being saved
* **Notion integration** — notes are written directly to your Notion database with full metadata (category, source, date, raw text)
* **Generic LLM layer** — swap Gemini for Claude or OpenAI by changing a single line in `llm.py`
* **Voice support** — coming in phase 2

---

## 🗂 Project Structure
```
think-drop/
├── main.py                 # Entry point
├── think_drop/
│   ├── bot.py              # Telegram bot handlers
│   ├── llm.py              # LLM abstraction (Gemini / Claude / OpenAI)
│   ├── notion.py           # Notion integration
│   └── config.py           # Environment variables
├── .env                    # Your secrets (not in git)
└── pyproject.toml
```

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
