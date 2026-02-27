"""Notion integration — uses python-notion-plus."""
from datetime import datetime, timezone

import pytz
from python_notion_plus import NotionClient
from think_drop.config import NOTION_API_KEY, NOTION_DATABASE_ID

_client = NotionClient(database_id=NOTION_DATABASE_ID, token=NOTION_API_KEY)


def write_note(title: str, summary: str, raw: str, category: str, source: str = "text") -> str:
    properties = {
        "Title": {
            "title": [{"text": {"content": title}}]
        },
        "Summary": {
            "rich_text": [{"text": {"content": summary}}]
        },
        "Raw": {
            "rich_text": [{"text": {"content": raw[:2000]}}]
        },
        "Category": {
            "select": {"name": category}
        },
        "Source": {
            "select": {"name": source}
        },
        "Date": {
            "date": {"start": datetime.now(timezone.utc).isoformat()}
            # "date": {"start": datetime.now(pytz.timezone("Asia/Jerusalem")).isoformat()}
        },
    }

    _client.add_row_to_db(notion_database_id=NOTION_DATABASE_ID, properties=properties)
    return f"https://notion.so/{NOTION_DATABASE_ID.replace('-', '')}"
