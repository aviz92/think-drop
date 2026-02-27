import anthropic

from think_drop.config import LLM_API_KEY
from think_drop.llms.base_llm import BaseLLM


class ClaudeLLM(BaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=LLM_API_KEY)

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            # model="claude-sonnet-4-6",
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
