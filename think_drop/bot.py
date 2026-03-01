"""Telegram bot — entry point for Think-Drop."""

import asyncio
import json
import uuid

from custom_python_logger import build_logger, get_logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from think_drop.config import get_settings
from think_drop.context import session_id as session_id_var
from think_drop.llm import classify_and_summarize
from think_drop.notion import write_note

logger = get_logger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # pylint: disable=W0613
    user = update.effective_user
    logger.info("Start command received | user_id=%s username=%s", user.id, user.username)
    await update.message.reply_text(
        "👋 Welcome to Think-Drop!\n\n"
        "Send me any note and I'll classify, summarize, and save it to Notion automatically."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # pylint: disable=W0613
    sid = str(uuid.uuid4())[:8]
    session_id_var.set(sid)

    user = update.effective_user
    text = update.message.text

    logger.info("[%s] Message received | user_id=%s username=%s | chars=%d", sid, user.id, user.username, len(text))

    await update.message.reply_text("⏳ Processing your note...")
    logger.debug("[%s] Processing acknowledgement sent", sid)

    try:
        logger.info("[%s] LLM classification started | provider=%s", sid, get_settings().llm_provider)
        result = await asyncio.to_thread(classify_and_summarize, text)
        logger.info("[%s] LLM classification done | title=%r category=%s", sid, result["title"], result["category"])

        title = result["title"]
        category = result["category"]
        summary = result["summary"]

        logger.info("[%s] Notion write started | title=%r category=%s", sid, title, category)
        notion_url = await asyncio.to_thread(
            write_note,
            title=title,
            summary=summary,
            raw=text,
            category=category,
            source="text",
        )
        logger.info("[%s] Note saved to Notion | url=%s", sid, notion_url)

        confirmation = (
            f"✅ Note saved to Notion!\n\n"
            f"📌 *{title}*\n"
            f"🏷 Category: {category}\n"
            f"📝 Summary: {summary}\n\n"
            f"🔗 [Open in Notion]({notion_url})"
        )
        await update.message.reply_text(confirmation, parse_mode="Markdown")
        logger.info("[%s] Confirmation sent to user", sid)

    except (json.JSONDecodeError, KeyError) as e:
        logger.error("[%s] LLM parse failed: %s", sid, e)
        await update.message.reply_text("❌ Couldn't understand the note. Please try rephrasing.")
    except Exception:
        logger.exception("[%s] Unexpected error processing message", sid)
        await update.message.reply_text("❌ Something went wrong. Please try again later.")


def run() -> None:
    build_logger("think-drop")
    app = ApplicationBuilder().token(get_settings().telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Think-Drop bot is running...")
    app.run_polling()


if __name__ == "__main__":
    run()
