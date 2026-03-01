from collections.abc import Generator

import pytest
from pydantic import ValidationError

from think_drop.config import CATEGORIES, get_settings
from think_drop.llms.const import LLMType


class TestSettings:
    def test_loads_gemini_provider(self, clear_settings_cache: Generator[None, None, None]) -> None:
        settings = get_settings()
        assert settings.llm_provider == LLMType.GEMINI
        assert settings.llm_api_key == "test_gemini_key"

    def test_llm_api_key_returns_correct_key_for_provider(
        self, clear_settings_cache: Generator[None, None, None], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "claude")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_claude_key")

        settings = get_settings()
        assert settings.llm_api_key == "test_claude_key"

    def test_missing_api_key_raises_validation_error(
        self, clear_settings_cache: Generator[None, None, None], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ValidationError, match="OPENAI_API_KEY"):
            get_settings()

    def test_invalid_provider_raises_validation_error(
        self, clear_settings_cache: Generator[None, None, None], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LLM_PROVIDER", "unknown_provider")

        with pytest.raises(ValidationError):
            get_settings()

    def test_categories_list_is_not_empty(self) -> None:
        assert len(CATEGORIES) > 0
        assert all(isinstance(c, str) for c in CATEGORIES)
