"""Generic LLM abstraction layer — swap providers by changing LLM_PROVIDER."""
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
