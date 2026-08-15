import os

from dotenv import load_dotenv

from services.llm.openai_provider import OpenAIProvider

load_dotenv()


class ProviderFactory:

    @staticmethod
    def create():

        provider = os.getenv("LLM_PROVIDER", "openai")

        if provider == "openai":
            return OpenAIProvider()

        raise ValueError(
            f"Proveedor no soportado: {provider}"
        )