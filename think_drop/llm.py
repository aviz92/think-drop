"""Generic LLM abstraction layer — swap providers by changing LLM_PROVIDER."""
import json
import google.generativeai as genai
from think_drop.config import GEMINI_API_KEY, CATEGORIES

LLM_PROVIDER = "gemini"  # Change to "claude" or "openai" in the future

genai.configure(api_key=GEMINI_API_KEY)
_gemini_model = genai.GenerativeModel("gemini-2.5-flash")


def _call_gemini(prompt: str) -> str:
    response = _gemini_model.generate_content(prompt)
    return response.text.strip()


def call_llm(prompt: str) -> str:
    """Single entry point — routes to the active LLM provider."""
    if LLM_PROVIDER == "gemini":
        return _call_gemini(prompt)
    raise NotImplementedError(f"LLM provider '{LLM_PROVIDER}' is not implemented yet.")


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

    raw = call_llm(prompt)

    # Strip markdown code fences if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
