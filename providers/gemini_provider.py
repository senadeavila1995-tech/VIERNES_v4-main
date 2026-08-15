from providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def ask(self, prompt: str):

        raise NotImplementedError(
            "Gemini aún no implementado."
        )