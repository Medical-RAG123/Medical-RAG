import os

from google.genai.errors import APIError, ServerError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class GeminiLLM:
    def __init__(self, client):
        self.client = client
        # Explicitly set model to gemini-2.5-flash to prevent defaulting to gemini-3.8-flash
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((ServerError, APIError)),
    )
    def generate(self, prompt: str, **kwargs):
        """Generates text via Gemini Chat API explicitly forcing gemini-2.5-flash."""
        chat = self.client.chats.create(model=self.model)
        response = chat.send_message(prompt)
        return response.text
