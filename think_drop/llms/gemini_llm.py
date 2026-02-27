from think_drop.config import LLM_API_KEY
from think_drop.llms.base_llm import BaseLLM


class GeminiLLM(BaseLLM):
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=LLM_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        return self.model.generate_content(prompt).text.strip()
