import os

from dotenv import load_dotenv
from openai import OpenAI

from services.llm.base_provider import BaseProvider

load_dotenv()


class OpenAIProvider(BaseProvider):

    def __init__(self):

        self.client = OpenAI(api_key=os.getenv("xxxxxxxxxxxxxxxxxxxxxx"))

        self.model = os.getenv("OPENAI_MODEL", "gpt-5")

    def ask(self, messages):

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0
        )

        return response.choices[0].message.content
