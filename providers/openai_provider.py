import os

from dotenv import load_dotenv
from openai import OpenAI

from providers.base_provider import BaseProvider

load_dotenv()


class OpenAIProvider(BaseProvider):

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "No se encontró OPENAI_API_KEY en el archivo .env"
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5"
        )

    def ask(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content