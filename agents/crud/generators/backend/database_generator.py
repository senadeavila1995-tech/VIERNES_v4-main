from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.module_resolver import ModuleResolver


class DatabaseGenerator(BaseGenerator):
    """
    Genera la capa Database del CRUD.

    La Database concreta conecta BaseDatabase
    con la sesión SQLAlchemy y el modelo ORM.
    """

    name = "database"

    description = "Genera la capa Database."

    order = 8

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_database(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_database(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.entity(context)

        database_class = f"{self.class_name(context)}Database"

        model_class = self.class_name(context)

        framework_import = ImportResolver.framework(
            "base_database",
            "BaseDatabase",
        )

        model_import = ImportResolver.build(
            ModuleResolver.model(entity),
            model_class,
        )

        return f'''"""
Database generado automáticamente por VIERNES.

Entidad:
{context.entity_name}
"""

from sqlalchemy.orm import Session

{framework_import}
{model_import}


class {database_class}(BaseDatabase):


    def __init__(
        self,
        session: Session,
    ):

        super().__init__(
            session,
            {model_class},
        )
'''
