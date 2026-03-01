import anthropic

from think_drop.config import get_settings
from think_drop.llms.base_llm import BaseLLM


class ClaudeLLM(BaseLLM):
    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=get_settings().llm_api_key)

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
