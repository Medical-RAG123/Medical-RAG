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

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((ServerError, APIError)),
    )
    def generate(self, prompt: str, **kwargs):
        # Force model to gemini-2.5-flash and use chats API to stop AFC warning
        chat = self.client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(prompt)
        return response.text
