import json
from unittest.mock import MagicMock, patch

import pytest

from think_drop.llm import _strip_markdown_fences, classify_and_summarize


class TestStripMarkdownFences:
    def test_plain_json_unchanged(self) -> None:
        text = '{"title": "T", "category": "Work", "summary": "S"}'
        assert _strip_markdown_fences(text) == text

    def test_strips_json_fences(self) -> None:
        text = '```json\n{"title": "T"}\n```'
        assert _strip_markdown_fences(text) == '{"title": "T"}'

    def test_strips_plain_fences(self) -> None:
        text = '```\n{"title": "T"}\n```'
        assert _strip_markdown_fences(text) == '{"title": "T"}'

    def test_strips_surrounding_whitespace(self) -> None:
        assert _strip_markdown_fences("  plain text  ") == "plain text"


class TestClassifyAndSummarize:
    def _make_mock_llm(self, response: str) -> MagicMock:
        mock_llm = MagicMock()
        mock_llm.generate.return_value = response
        return mock_llm

    def test_valid_plain_json(self) -> None:
        payload = {"title": "Test Note", "category": "Work", "summary": "A summary."}
        mock_llm = self._make_mock_llm(json.dumps(payload))

        with patch("think_drop.llm.get_llm", return_value=mock_llm):
            result = classify_and_summarize("This is a work note.")

        assert result == payload

    def test_valid_fenced_json(self) -> None:
        payload = {"title": "Idea", "category": "Ideas", "summary": "A great idea."}
        fenced = f"```json\n{json.dumps(payload)}\n```"
        mock_llm = self._make_mock_llm(fenced)

        with patch("think_drop.llm.get_llm", return_value=mock_llm):
            result = classify_and_summarize("Some note text.")

        assert result["title"] == "Idea"
        assert result["category"] == "Ideas"

    def test_raises_on_invalid_json(self) -> None:
        mock_llm = self._make_mock_llm("not valid json at all")

        with patch("think_drop.llm.get_llm", return_value=mock_llm):
            with pytest.raises(json.JSONDecodeError):
                classify_and_summarize("Some note.")

    def test_passes_text_to_llm(self) -> None:
        payload = {"title": "T", "category": "Work", "summary": "S"}
        mock_llm = self._make_mock_llm(json.dumps(payload))

        with patch("think_drop.llm.get_llm", return_value=mock_llm):
            classify_and_summarize("My specific note text.")

        call_args = mock_llm.generate.call_args[0][0]
        assert "My specific note text." in call_args
