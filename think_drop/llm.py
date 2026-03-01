"""Generic LLM abstraction layer — swap providers by changing LLM_PROVIDER."""

import json
import re
from functools import cache

from custom_python_logger import get_logger
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_exponential

from think_drop.config import CATEGORIES, get_settings
from think_drop.context import session_id as session_id_var
from think_drop.llms.base_llm import BaseLLM
from think_drop.llms.claude_llm import ClaudeLLM
from think_drop.llms.gemini_llm import GeminiLLM
from think_drop.llms.openai_lm import OpenAILLM

logger = get_logger(__name__)

_PROVIDERS_MAP = {
    "gemini": GeminiLLM,
    "claude": ClaudeLLM,
    "openai": OpenAILLM,
}


@cache
def get_llm() -> BaseLLM:
    if (provider := get_settings().llm_provider) not in _PROVIDERS_MAP:
        raise NotImplementedError(
            f"LLM provider '{provider}' is not supported. Choose from: {list(_PROVIDERS_MAP.keys())}"
        )
    return _PROVIDERS_MAP[provider]()


def _strip_markdown_fences(text: str) -> str:
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text.strip())
    return match.group(1).strip() if match else text.strip()


@retry(
    retry=retry_if_not_exception_type((json.JSONDecodeError, KeyError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
def classify_and_summarize(text: str) -> dict[str, str]:
    """Returns {category, summary, title} for a given note."""
    sid = session_id_var.get()
    categories_str = ", ".join(CATEGORIES)

    logger.debug("[%s] Building prompt | text_chars=%d categories=%d", sid, len(text), len(CATEGORIES))

    prompt = f"""You are a personal note-taking assistant.

Given the following note, return a JSON object with exactly these fields:
- "title": a short title (max 8 words)
- "category": the most fitting category from this list: {categories_str}
- "summary": a clean, concise summary of the note (1-3 sentences)

Note:
{text}

Return only valid JSON, no markdown, no explanation."""

    logger.debug("[%s] Sending prompt to LLM", sid)
    raw = get_llm().generate(prompt)
    logger.debug("[%s] LLM response received | response_chars=%d", sid, len(raw))

    parsed = json.loads(_strip_markdown_fences(raw))
    logger.debug("[%s] Response parsed successfully | keys=%s", sid, list(parsed.keys()))
    return parsed
