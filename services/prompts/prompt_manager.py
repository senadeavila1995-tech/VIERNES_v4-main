from pathlib import Path


class PromptManager:

    def __init__(self):

        self.base = Path("prompts")

    def load(self, name: str) -> str:

        file = self.base / f"{name}.md"

        if not file.exists():
            raise FileNotFoundError(
                f"No existe el prompt '{name}'."
            )

        return file.read_text(
            encoding="utf-8"
        )

    def render(self, name: str, **kwargs):

        prompt = self.load(name)

        for key, value in kwargs.items():

            prompt = prompt.replace(
                "{{" + key + "}}",
                str(value)
            )

        return prompt