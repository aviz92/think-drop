import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from think_drop.bot import handle_message, start


def _make_update(text: str = "Test note", user_id: int = 123, username: str = "testuser") -> MagicMock:
    update = MagicMock()
    update.effective_user.id = user_id
    update.effective_user.username = username
    update.message.text = text
    update.message.reply_text = AsyncMock()
    return update


_LLM_RESULT = {"title": "Test Title", "category": "Work", "summary": "A test summary."}
_NOTION_URL = "https://notion.so/abc123"


class TestStartHandler:
    @pytest.mark.anyio
    async def test_sends_welcome_message(self) -> None:
        update = _make_update()
        await start(update, MagicMock())

        update.message.reply_text.assert_called_once()
        welcome_text = update.message.reply_text.call_args[0][0]
        assert "Think-Drop" in welcome_text


class TestHandleMessage:
    @pytest.mark.anyio
    async def test_happy_path_sends_two_replies(self) -> None:
        update = _make_update("Buy milk and eggs")

        with (
            patch("think_drop.bot.classify_and_summarize", return_value=_LLM_RESULT),
            patch("think_drop.bot.write_note", return_value=_NOTION_URL),
        ):
            await handle_message(update, MagicMock())

        assert update.message.reply_text.call_count == 2

    @pytest.mark.anyio
    async def test_happy_path_confirmation_contains_title(self) -> None:
        update = _make_update("Some note")

        with (
            patch("think_drop.bot.classify_and_summarize", return_value=_LLM_RESULT),
            patch("think_drop.bot.write_note", return_value=_NOTION_URL),
        ):
            await handle_message(update, MagicMock())

        confirmation = update.message.reply_text.call_args_list[1][0][0]
        assert "Test Title" in confirmation
        assert "Work" in confirmation

    @pytest.mark.anyio
    async def test_json_parse_error_sends_rephrase_message(self) -> None:
        update = _make_update("Some note")

        with patch(
            "think_drop.bot.classify_and_summarize",
            side_effect=json.JSONDecodeError("msg", "doc", 0),
        ):
            await handle_message(update, MagicMock())

        error_reply = update.message.reply_text.call_args_list[1][0][0]
        assert "rephrasing" in error_reply.lower()

    @pytest.mark.anyio
    async def test_unexpected_error_sends_generic_message(self) -> None:
        update = _make_update("Some note")

        with patch(
            "think_drop.bot.classify_and_summarize",
            side_effect=RuntimeError("API down"),
        ):
            await handle_message(update, MagicMock())

        error_reply = update.message.reply_text.call_args_list[1][0][0]
        assert "went wrong" in error_reply.lower()

    @pytest.mark.anyio
    async def test_error_reply_does_not_leak_internal_details(self) -> None:
        update = _make_update("Some note")

        with patch(
            "think_drop.bot.classify_and_summarize",
            side_effect=RuntimeError("secret internal error message"),
        ):
            await handle_message(update, MagicMock())

        error_reply = update.message.reply_text.call_args_list[1][0][0]
        assert "secret internal error message" not in error_reply
