from pathlib import Path


class TemplateEngine:

    @staticmethod
    def render(
        template_path: Path,
        context: dict,
    ) -> str:

        content = template_path.read_text(encoding="utf-8")

        for key, value in context.items():
            content = content.replace("{{" + key.upper() + "}}", str(value))

        return content
