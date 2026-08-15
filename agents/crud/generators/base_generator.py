from abc import ABC, abstractmethod

from agents.crud.models.generated_file import GeneratedFile
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.folder_resolver import FolderResolver
from agents.crud.resolvers.naming_resolver import NamingResolver


class BaseGenerator(ABC):
    """
    Clase base para todos los generadores del motor CRUD.

    Responsabilidades:

    - Coordinar el flujo de generación.
    - Construir objetos GeneratedFile.
    - Resolver nombres.
    - Resolver carpetas lógicas.
    - Proporcionar helpers comunes.

    No debe:

    - Escribir archivos.
    - Crear carpetas físicas.
    - Manejar rutas reales.
    """

    # ==========================================================
    # Metadatos
    # ==========================================================

    name: str = "base"

    description: str = "Generador base"

    order: int = 0

    writes_file: bool = True

    # ==========================================================
    # Flujo principal
    # ==========================================================

    def generate(
        self,
        context: GenerationContext,
    ) -> GeneratedFile:

        if not self.validate(context):
            raise ValueError(f"El generador '{self.name}' no puede ejecutarse.")

        return self.build_file(
            entity=context.entity_name,
            folder=self.folder(),
            filename=self.filename(context),
            content=self.generate_content(context),
            description=self.description,
        )

    # ==========================================================
    # Obligatorio para hijos
    # ==========================================================

    @abstractmethod
    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:
        """
        Cada Generator implementa únicamente
        la construcción del contenido.
        """
        raise NotImplementedError()

    # ==========================================================
    # Validación
    # ==========================================================

    def validate(
        self,
        context: GenerationContext,
    ) -> bool:

        return bool(context.entity_name)

    # ==========================================================
    # Construcción del GeneratedFile
    # ==========================================================

    def build_file(
        self,
        *,
        entity: str,
        folder: str,
        filename: str,
        content: str,
        description: str = "",
        overwrite: bool = True,
        encoding: str = "utf-8",
    ) -> GeneratedFile:

        return GeneratedFile(
            entity=entity,
            layer=self.layer(),
            folder=folder,
            filename=filename,
            content=content,
            overwrite=overwrite,
            encoding=encoding,
            description=description,
        )

    # ==========================================================
    # Resolución de carpeta
    # ==========================================================

    def folder(self) -> str:

        return FolderResolver.resolve(self.name)

    # ==========================================================
    # Resolución de archivo
    # ==========================================================

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return NamingResolver.filename(
            context.entity_name,
            self.name,
        )

    # ==========================================================
    # Helpers de contexto
    # ==========================================================

    def entity(
        self,
        context: GenerationContext,
    ) -> str:

        return NamingResolver.snake(
            context.entity_name,
        )

    def table(
        self,
        context: GenerationContext,
    ) -> str:

        return context.table_name.strip().lower()

    # ==========================================================
    # Helpers de nombres
    # ==========================================================

    def class_name(
        self,
        context: GenerationContext,
        kind: str = "model",
    ) -> str:
        """
        Devuelve el nombre de cualquier clase
        generada por el motor CRUD.
        """

        return NamingResolver.class_name(
            context.entity_name,
            kind,
        )

    def snake_name(
        self,
        context: GenerationContext,
    ) -> str:

        return NamingResolver.snake(
            context.entity_name,
        )

    def camel_name(
        self,
        context: GenerationContext,
    ) -> str:

        return NamingResolver.camel(
            context.entity_name,
        )

    def pascal_name(
        self,
        context: GenerationContext,
    ) -> str:

        return NamingResolver.pascal(
            context.entity_name,
        )
        # ==========================================================

    # Helpers específicos de clases
    # ==========================================================

    def controller_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "controller",
        )

    def service_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "service",
        )

    def repository_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "repository",
        )

    def validator_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "validator",
        )

    def schema_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "schema",
        )

    def database_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "database",
        )

    def dto_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "dto",
        )

    def view_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "view",
        )

    def route_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.class_name(
            context,
            "route",
        )

    def layer(self) -> str:
        """
        Devuelve la capa del generador.

        backend
        frontend
        """

        return FolderResolver.layer(self.name)
