from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProjectContext:
    """
    Contiene la configuración general
    del proyecto donde se generará el CRUD.

    Responsabilidades:
    - Información del proyecto.
    - Tecnologías utilizadas.
    - Configuración general de generación.

    No administra carpetas CRUD.
    La estructura de generación pertenece a CRUD_STRUCTURE.
    """

    # ==========================================================
    # Información general
    # ==========================================================

    project_name: str

    root_path: Path

    # ==========================================================
    # Tecnologías
    # ==========================================================

    language: str = "python"

    framework: str = "fastapi"

    database: str = "mysql"

    orm: str = "sqlalchemy"

    # ==========================================================
    # Opciones de generación
    # ==========================================================

    overwrite: bool = False

    use_templates: bool = True

    create_tests: bool = False

    create_docs: bool = False

    # ==========================================================
    # Rutas generales
    # ==========================================================

    source_dir: str = "src"

    @property
    def source_path(self) -> Path:
        """
        Carpeta principal del código fuente.

        Ejemplo:

        proyecto/
            src/
        """

        return self.root_path / self.source_dir

    # ==========================================================
    # Información auxiliar
    # ==========================================================

    @property
    def project_path(self) -> Path:
        """
        Ruta raíz del proyecto.
        """

        return self.root_path
