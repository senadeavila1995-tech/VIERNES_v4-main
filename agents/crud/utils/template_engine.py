from pathlib import Path


class TemplateEngine:
    """
    Motor simple de reemplazo de variables en templates.
    """

    @staticmethod
    def render(
        template_path: Path,
        context: dict,
    ) -> str:

        content = template_path.read_text(encoding="utf-8")

        for key, value in context.items():
            placeholder = "{{" + key.upper() + "}}"
            content = content.replace(placeholder, str(value))

        return content
