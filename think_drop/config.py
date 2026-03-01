"""Application settings — loaded lazily from environment variables or .env file."""

from functools import cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from think_drop.llms.const import LLMType

CATEGORIES = [
    "Work",
    "Home",
    "Ideas",
    "Shopping",
    "Meetings",
    "Reading",
    "Decisions",
    "Personal",
]


class Settings(BaseSettings):
    telegram_bot_token: str
    notion_token: str
    notion_db_id: str
    llm_provider: LLMType
    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None  # maps to ANTHROPIC_API_KEY (standard Anthropic SDK var)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", frozen=True)

    @model_validator(mode="after")
    def check_api_key_for_provider(self) -> "Settings":
        required: dict[LLMType, str | None] = {
            LLMType.GEMINI: self.gemini_api_key,
            LLMType.OPENAI: self.openai_api_key,
            LLMType.CLAUDE: self.anthropic_api_key,
        }
        if not required[self.llm_provider]:
            raise ValueError(f"{self.llm_provider.upper()}_API_KEY is required when LLM_PROVIDER={self.llm_provider}")
        return self

    @property
    def llm_api_key(self) -> str:
        key_map: dict[LLMType, str | None] = {
            LLMType.GEMINI: self.gemini_api_key,
            LLMType.OPENAI: self.openai_api_key,
            LLMType.CLAUDE: self.anthropic_api_key,
        }
        return key_map[self.llm_provider]  # type: ignore[return-value]


@cache
def get_settings() -> Settings:
    return Settings()
