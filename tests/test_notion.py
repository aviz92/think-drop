from unittest.mock import MagicMock, patch

import pytest

from think_drop import notion
from think_drop.notion import write_note


@pytest.fixture(autouse=True)
def reset_notion_client_cache() -> None:
    """Ensure _get_client() is not cached across tests."""
    notion._get_client.cache_clear()  # pylint: disable=protected-access


class TestWriteNote:
    def _mock_client(self, page_id: str = "abc-123-def-456") -> MagicMock:
        mock_client = MagicMock()
        mock_client.client.pages.create.return_value = {"id": page_id}
        return mock_client

    def test_returns_notion_page_url(self) -> None:
        with patch("think_drop.notion._get_client", return_value=self._mock_client()):
            result = write_note("Buy milk", "Summary text", "Raw note", "Shopping")

        assert result == "https://notion.so/abc123def456"

    def test_truncates_raw_to_2000_chars(self) -> None:
        mock_client = self._mock_client()
        long_raw = "x" * 3000

        with patch("think_drop.notion._get_client", return_value=mock_client):
            write_note("Title", "Summary", long_raw, "Work")

        call_kwargs = mock_client.client.pages.create.call_args[1]
        raw_content = call_kwargs["properties"]["Raw"]["rich_text"][0]["text"]["content"]
        assert len(raw_content) == 2000

    def test_sets_correct_category(self) -> None:
        mock_client = self._mock_client()

        with patch("think_drop.notion._get_client", return_value=mock_client):
            write_note("Title", "Summary", "Raw", "Ideas")

        call_kwargs = mock_client.client.pages.create.call_args[1]
        assert call_kwargs["properties"]["Category"]["select"]["name"] == "Ideas"

    def test_sets_default_source_to_text(self) -> None:
        mock_client = self._mock_client()

        with patch("think_drop.notion._get_client", return_value=mock_client):
            write_note("Title", "Summary", "Raw", "Work")

        call_kwargs = mock_client.client.pages.create.call_args[1]
        assert call_kwargs["properties"]["Source"]["select"]["name"] == "text"

    def test_uses_correct_database_id(self) -> None:
        mock_client = self._mock_client()

        with patch("think_drop.notion._get_client", return_value=mock_client):
            write_note("Title", "Summary", "Raw", "Work")

        call_kwargs = mock_client.client.pages.create.call_args[1]
        assert call_kwargs["parent"]["database_id"] == "test-db-id-1234"
