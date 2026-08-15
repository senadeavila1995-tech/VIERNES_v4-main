from pathlib import Path


class TemplateResolver:
    """
    Resuelve la ubicación de los templates del motor CRUD.
    """

    BASE_DIR = Path(__file__).resolve().parents[1] / "generators" / "templates"

    @classmethod
    def backend(
        cls,
        template: str,
    ) -> Path:

        return cls.BASE_DIR / "backend" / template

    @classmethod
    def frontend(
        cls,
        template: str,
    ) -> Path:

        return cls.BASE_DIR / "frontend" / template
