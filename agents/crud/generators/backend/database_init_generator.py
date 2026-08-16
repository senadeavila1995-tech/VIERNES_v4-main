from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext


class DatabaseInitGenerator(BaseGenerator):
    """
    Genera la inicialización de la base de datos.

    Registra los modelos SQLAlchemy y crea las tablas.
    """

    name = "database_init"

    description = "Genera inicializador de base de datos."

    order = 130

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        imports = []

        definition = context.definition

        module = self.snake_name_from_definition(
            definition
        )

        entity = self.class_name_from_definition(
            definition
        )

        imports.append(
            f"from backend.modules.{module}.models.{module} "
            f"import {entity}"
        )

        imports_text = "\n".join(imports)

        return f'''"""
Inicialización automática de base de datos.
Generado por VIERNES.
"""

from backend.framework.base_model import Base
from backend.framework.database.connection import engine

{imports_text}


def init_database():

    Base.metadata.create_all(
        bind=engine
    )
'''

    def generate(
        self,
        context: GenerationContext,
    ):

        return self.build_file(
            entity="",
            folder="framework/database",
            filename="init_database.py",
            content=self.generate_content(context),
            description=self.description,
        )

    def snake_name_from_definition(
        self,
        definition,
    ):

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.snake(
            definition.entity
        )

    def class_name_from_definition(
        self,
        definition,
    ):

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.class_name(
            definition.entity
        )


    def validate(
        self,
        context: GenerationContext,
    ):

        return bool(
            getattr(
                context,
                "definition",
                None,
            )
        )
