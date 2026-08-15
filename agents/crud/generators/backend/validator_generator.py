from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.module_resolver import ModuleResolver


class ValidatorGenerator(BaseGenerator):
    """
    Genera la capa Validator.

    El Validator únicamente conecta
    BaseValidator con el esquema
    generado para la entidad.
    """

    name = "validator"

    description = "Genera el validador del modelo."

    order = 4

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_validator(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_validator(
        self,
        context: GenerationContext,
    ) -> str:

        validator = self.validator_name(context)

        framework_import = ImportResolver.framework(
            "base_validator",
            "BaseValidator",
        )

        schema_import = ImportResolver.build(
            ModuleResolver.schema(
                self.entity(context),
            ),
            "SCHEMA",
        )

        return f"""{framework_import}
{schema_import}


class {validator}(BaseValidator):


    schema = SCHEMA
"""
