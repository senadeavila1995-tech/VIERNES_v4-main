from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider
from providers.gemini_provider import GeminiProvider
from providers.claude_provider import ClaudeProvider


class LLMManager:

    def __init__(self):

        self.providers = {

            "openai": OpenAIProvider(),

            "ollama": OllamaProvider(),

            "gemini": GeminiProvider(),

            "claude": ClaudeProvider()

        }

        self.default = "ollama"

    def ask(

        self,

        prompt,

        provider=None

    ):

        if provider is None:

            provider = self.default

        llm = self.providers.get(provider)

        if llm is None:

            raise Exception(

                f"No existe el proveedor {provider}"

            )

        return llm.ask(prompt)