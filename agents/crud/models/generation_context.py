from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .crud_definition import CrudDefinition
from .project_context import ProjectContext


@dataclass(slots=True)
class GenerationContext:
    """
    Contexto completo de una generación CRUD.

    Contiene:

    - Definición de la entidad.
    - Configuración del proyecto.
    - Estado de ejecución.
    - Información compartida entre generators.

    No genera archivos.
    No escribe archivos.
    No crea carpetas.
    """

    # ==========================================================
    # Configuración principal
    # ==========================================================

    definition: CrudDefinition

    project: ProjectContext

    # ==========================================================
    # Definiciones disponibles
    # ==========================================================

    definitions: dict[str, CrudDefinition] = field(
        default_factory=dict
    )

    # ==========================================================
    # Información ejecución
    # ==========================================================

    created_at: datetime = field(default_factory=datetime.now)

    # ==========================================================
    # Estado generación
    # ==========================================================

    generated_files: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    # ==========================================================
    # Extensión para plugins
    # ==========================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Accesos rápidos
    # ==========================================================

    @property
    def entity_name(self) -> str:
        """
        Nombre de la entidad.
        """

        return self.definition.entity

    @property
    def table_name(self) -> str:
        """
        Nombre de la tabla.
        """

        return self.definition.table

    @property
    def fields(self):
        """
        Campos definidos para el CRUD.
        """

        return self.definition.fields

    # ==========================================================
    # Registro de resultados
    # ==========================================================

    def add_generated_file(self, path: str) -> None:

        self.generated_files.append(path)

    def add_warning(self, message: str) -> None:

        self.warnings.append(message)

    def add_error(self, message: str) -> None:

        self.errors.append(message)

    # ==========================================================
    # Metadata
    # ==========================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(key, default)

    # ==========================================================
    # Estado
    # ==========================================================

    @property
    def has_errors(self) -> bool:

        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:

        return bool(self.warnings)
