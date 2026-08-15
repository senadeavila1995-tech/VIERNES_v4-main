from services.llm.provider_factory import ProviderFactory


class OpenAIService:

    def __init__(self):

        self.provider = ProviderFactory.create()

    def ask(self, messages):

        return self.provider.ask(messages)