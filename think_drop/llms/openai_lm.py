from openai import OpenAI

from think_drop.config import get_settings
from think_drop.llms.base_llm import BaseLLM


class OpenAILLM(BaseLLM):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=get_settings().llm_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
