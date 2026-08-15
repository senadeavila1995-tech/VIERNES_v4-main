from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class GeneratedFile:
    """
    Representa un archivo generado por cualquier Generator.

    El Generator únicamente construye esta clase.
    El FileWriter es el encargado de escribirlo.
    """

    entity: str

    # backend | frontend
    layer: str

    folder: str

    filename: str

    content: str

    overwrite: bool = True

    encoding: str = "utf-8"

    description: str = ""

    @property
    def extension(self) -> str:
        return Path(self.filename).suffix

    @property
    def stem(self) -> str:
        return Path(self.filename).stem

    @property
    def is_python(self) -> bool:
        return self.extension == ".py"

    @property
    def is_typescript(self) -> bool:
        return self.extension == ".ts"

    @property
    def is_javascript(self) -> bool:
        return self.extension == ".js"

    @property
    def relative_path(self) -> Path:
        """
        Ruta relativa dentro de la aplicación.

        backend/controllers/producto_controller.py
        frontend/pages/ProductoPage.tsx
        """

        return Path(self.layer) / self.folder / self.filename

    def __str__(self) -> str:
        return str(self.relative_path)
