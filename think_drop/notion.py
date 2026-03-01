"""Notion integration — uses python-notion-plus."""

from datetime import datetime
from functools import cache

import pytz
from custom_python_logger import get_logger
from python_notion_plus import NotionClient

from think_drop.config import get_settings
from think_drop.context import session_id as session_id_var

logger = get_logger(__name__)


@cache
def _get_client() -> NotionClient:
    settings = get_settings()
    return NotionClient(database_id=settings.notion_db_id, token=settings.notion_token)


def write_note(title: str, summary: str, raw: str, category: str, source: str = "text") -> str:
    sid = session_id_var.get()
    settings = get_settings()
    logger.debug("[%s] Creating Notion page | title=%r category=%s source=%s", sid, title, category, source)

    properties = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Summary": {"rich_text": [{"text": {"content": summary}}]},
        "Raw": {"rich_text": [{"text": {"content": raw[:2000]}}]},
        "Category": {"select": {"name": category}},
        "Source": {"select": {"name": source}},
        "Date": {"date": {"start": datetime.now(pytz.timezone("Asia/Jerusalem")).isoformat()}},
    }

    page = _get_client().client.pages.create(
        parent={"database_id": settings.notion_db_id},
        properties=properties,
    )
    page_id = page["id"]
    logger.debug("[%s] Notion page created | page_id=%s", sid, page_id)
    return f"https://notion.so/{page_id.replace('-', '')}"
