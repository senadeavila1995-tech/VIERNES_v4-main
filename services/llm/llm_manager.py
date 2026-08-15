from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider
from providers.gemini_provider import GeminiProvider
from providers.claude_provider import ClaudeProvider


class LLMManager:

    def __init__(self):

        self.providers = {}

        self.provider_classes = {

            "openai": OpenAIProvider,

            "ollama": OllamaProvider,

            "gemini": GeminiProvider,

            "claude": ClaudeProvider

        }

        self.default = "ollama"


    def get_provider(self, name):

        if name not in self.providers:

            provider_class = self.provider_classes.get(name)

            if provider_class is None:

                raise Exception(
                    f"No existe el proveedor {name}"
                )

            self.providers[name] = provider_class()

        return self.providers[name]


    def ask(
        self,
        prompt,
        provider=None
    ):

        if provider is None:

            provider = self.default


        llm = self.get_provider(provider)


        return llm.ask(prompt)
