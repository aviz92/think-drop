from collections.abc import Generator

import pytest

from think_drop.config import get_settings


@pytest.fixture(autouse=True)
def isolate_settings(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Force test env vars and clear the settings cache before/after every test.

    Prevents real .env values (e.g. LLM_PROVIDER=claude) from leaking into
    tests and ensures each test starts with a known, clean configuration.
    """
    get_settings.cache_clear()

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_telegram_token")
    monkeypatch.setenv("NOTION_TOKEN", "test_notion_token")
    monkeypatch.setenv("NOTION_DB_ID", "test-db-id-1234")
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key")

    yield

    get_settings.cache_clear()


@pytest.fixture()
def clear_settings_cache() -> Generator[None, None, None]:
    """Explicit cache-clear for config tests that override specific env vars."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
