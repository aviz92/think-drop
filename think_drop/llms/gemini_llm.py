from google import genai

from think_drop.config import get_settings
from think_drop.llms.base_llm import BaseLLM


class GeminiLLM(BaseLLM):
    def __init__(self) -> None:
        self.client = genai.Client(api_key=get_settings().llm_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text.strip()
