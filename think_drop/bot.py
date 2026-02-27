"""Telegram bot — entry point for Think-Drop."""
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from think_drop.config import TELEGRAM_BOT_TOKEN
from think_drop.llm import classify_and_summarize
from think_drop.notion import write_note

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome to Think-Drop!\n\nSend me any note and I'll classify, summarize, and save it to Notion automatically."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text("⏳ Processing your note...")

    try:
        result = classify_and_summarize(text)
        print(f'LLM Result: {result}')  # Debugging output
        title = result["title"]
        category = result["category"]
        summary = result["summary"]

        notion_url = write_note(
            title=title,
            summary=summary,
            raw=text,
            category=category,
            source="text",
        )

        confirmation = (
            f"✅ Note saved to Notion!\n\n"
            f"📌 *{title}*\n"
            f"🏷 Category: {category}\n"
            f"📝 Summary: {summary}\n\n"
            f"🔗 [Open in Notion]({notion_url})"
        )
        await update.message.reply_text(confirmation, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(f"❌ Something went wrong: {str(e)}")


def run():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Think-Drop bot is running...")
    app.run_polling()


if __name__ == "__main__":
    run()
