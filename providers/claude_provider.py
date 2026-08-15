from providers.base_provider import BaseProvider


class ClaudeProvider(BaseProvider):

    def ask(self, prompt: str):

        raise NotImplementedError(
            "Claude aún no implementado."
        )