import os

from app.api.ai.llms.gemini import GeminiLLM
from google import genai


class LLMFactory:
    @staticmethod
    def create(provider: str = "gemini"):
        if provider.lower() == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            client = genai.Client(api_key=api_key)
            return GeminiLLM(client)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
