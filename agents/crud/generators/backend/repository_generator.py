from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.module_resolver import ModuleResolver


class RepositoryGenerator(BaseGenerator):
    """
    Genera la capa Repository.

    El Repository únicamente conecta el
    BaseRepository con la implementación
    concreta de Database.
    """

    name = "repository"

    description = "Genera la capa Repository."

    order = 5

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_repository(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_repository(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.entity(context)

        repository = self.repository_name(context)

        database = self.class_name(context) + "Database"

        framework_import = ImportResolver.framework(
            "base_repository",
            "BaseRepository",
        )

        database_import = ImportResolver.build(
            ModuleResolver.database(entity),
            database,
        )

        return f"""from sqlalchemy.orm import Session

{framework_import}
{database_import}


class {repository}(BaseRepository):


    def __init__(
        self,
        session: Session,
    ):

        super().__init__(
            {database}(
                session
            )
        )
"""
