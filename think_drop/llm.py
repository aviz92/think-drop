"""Generic LLM abstraction layer — swap providers by changing LLM_PROVIDER."""
import json
from think_drop.config import CATEGORIES, LLM_PROVIDER
from think_drop.llms.base_llm import BaseLLM
from think_drop.llms.claude_llm import ClaudeLLM
from think_drop.llms.gemini_llm import GeminiLLM
from think_drop.llms.openai_lm import OpenAILLM

_PROVIDERS_MAP = {
    "gemini": GeminiLLM,
    "claude": ClaudeLLM,
    "openai": OpenAILLM,
}


def get_llm() -> BaseLLM:
    if LLM_PROVIDER not in _PROVIDERS_MAP:
        raise NotImplementedError(
            f"LLM provider '{LLM_PROVIDER}' is not supported. Choose from: {list(_PROVIDERS_MAP.keys())}")
    return _PROVIDERS_MAP[LLM_PROVIDER]()


def classify_and_summarize(text: str) -> dict:
    """Returns {category, summary, title} for a given note."""
    categories_str = ", ".join(CATEGORIES)
    prompt = f"""You are a personal note-taking assistant.

Given the following note, return a JSON object with exactly these fields:
- "title": a short title (max 8 words)
- "category": the most fitting category from this list: {categories_str}
- "summary": a clean, concise summary of the note (1-3 sentences)

Note:
{text}

Return only valid JSON, no markdown, no explanation."""

    raw = get_llm().generate(prompt)

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
