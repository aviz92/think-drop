[![Python](https://img.shields.io/badge/python-%3E=3.12-blue)](https://www.python.org/)
[![Development Status](https://img.shields.io/badge/status-stable-green)](https://github.com/aviz92/think-drop)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)](https://github.com/aviz92/think-drop)
[![License](https://img.shields.io/github/license/aviz92/think-drop)](LICENSE)

---

# 💡 think-drop
A personal Telegram bot that captures your text notes, classifies them by category, and writes clean summaries directly to your Notion workspace — powered by AI.

---

## 📦 Installation

Clone and install dependencies:
```bash
git clone https://github.com/aviz92/think-drop.git
cd think-drop
uv sync
```

Or run with Docker Compose:
```bash
docker-compose up --build
```

Run in the background:
```bash
docker-compose up --build -d
docker-compose down
```

---

## 🚀 Features
  - ✅ **Auto-classification** — AI classifies each note into a category (Work, Home, Ideas, Shopping, Meetings, Reading, Decisions, Personal)
  - ✅ **Smart summarization** — every note gets a concise title and summary before being saved
  - ✅ **Notion integration** — notes are written directly to your Notion database with full metadata (title, summary, raw text, category, source, date)
  - ✅ **Multi-LLM support** — switch between Gemini, OpenAI, or Claude by changing a single env var (`LLM_PROVIDER`)
  - ✅ **Session-scoped logging** — every message processing pipeline is tracked with a unique session ID for easy debugging and tracing
  - ✅ **Async processing** — LLM and Notion calls run off the event loop, keeping the bot responsive under load

---

## ⚙️ Configuration

Create a `.env` file with the following variables:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

NOTION_TOKEN=your_notion_internal_integration_secret
NOTION_DB_ID=your_notion_database_id

LLM_PROVIDER=gemini          # options: gemini | openai | claude
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Only the API key matching your chosen `LLM_PROVIDER` is required.

---

## 🛠️ How to Use

### 🤖 Creating a Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send the command `/newbot`.
3. Follow the prompts to name your bot and choose a username.
4. Copy the Bot Token and add it to your `.env` as `TELEGRAM_BOT_TOKEN`.

### 🧠 LLM API Key
Choose one provider and set the matching env var:

| Provider | `LLM_PROVIDER` value | Env var | Where to get it |
|----------|----------------------|---------|-----------------|
| Google Gemini | `gemini` | `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| OpenAI | `openai` | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) |
| Anthropic Claude | `claude` | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |

### 🧩 Setting Up Notion Integration
1. **Create an integration token**
   - Go to [notion.so/my-integrations](https://www.notion.so/profile/integrations/internal) → click **+ New integration**.
   - Give it a name, select your workspace, and save the generated **Internal Integration Token** as `NOTION_TOKEN`.

2. **Create a Notion database** with the following properties:

   | Property | Type |
   |----------|------|
   | Title | title |
   | Summary | text |
   | Raw | text |
   | Category | select |
   | Source | select |
   | Date | date |

3. **Connect the integration** — open the database in Notion, click ··· → **Connections** and add your integration.

4. **Get the database ID** — open the database as a full page. The ID is the segment before `?v=` in the URL:
   `notion.so/<DATABASE-ID>?v=...`

---

## 🚀 Quick Start

```bash
uv run python think_drop/main.py
```

Then open Telegram, find your bot and send `/start`.

---

## 📋 Log Tracing

Every message is assigned a unique 8-character session ID. All log lines for that message share the same ID, making it easy to trace a full request through the pipeline:

```
INFO  [a3f2c1b8] Message received | user_id=123456 username=avi | chars=47
INFO  [a3f2c1b8] LLM classification started | provider=gemini
DEBUG [a3f2c1b8] LLM response received | response_chars=112
INFO  [a3f2c1b8] LLM classification done | title='Buy milk' category=Shopping
INFO  [a3f2c1b8] Notion write started | title='Buy milk' category=Shopping
INFO  [a3f2c1b8] Note saved to Notion | url=https://notion.so/abc123...
INFO  [a3f2c1b8] Confirmation sent to user
```

---

## 🤝 Contributing

If you have a helpful pattern or improvement to suggest:
1. Fork the repo
2. Create a new branch
3. Submit a pull request

I welcome additions that promote clean, productive, and maintainable development.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Thanks

Thanks for exploring this repository!
Happy coding!
