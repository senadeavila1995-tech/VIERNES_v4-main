from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.module_resolver import ModuleResolver


class ServiceGenerator(BaseGenerator):
    """
    Genera la capa Service del CRUD.

    El Service únicamente conecta el
    BaseService con el Repository concreto.
    """

    name = "service"

    description = "Genera la capa Service."

    order = 6

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_service(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_service(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.entity(context)

        service = self.service_name(context)

        repository = self.repository_name(context)

        framework_import = ImportResolver.framework(
            "base_service",
            "BaseService",
        )

        repository_import = ImportResolver.build(
            ModuleResolver.resolve(
                entity,
                "repository",
            ),
            repository,
        )

        return f"""from sqlalchemy.orm import Session

{framework_import}
{repository_import}


class {service}(BaseService):


    def __init__(
        self,
        session: Session,
    ):

        super().__init__(
            {repository}(
                session
            )
        )
"""
