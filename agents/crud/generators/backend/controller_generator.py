from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.module_resolver import ModuleResolver


class ControllerGenerator(BaseGenerator):
    """
    Genera la capa Controller.

    El Controller únicamente conecta
    BaseController con el Service y
    el Validator concretos.
    """

    name = "controller"

    description = "Genera el controlador."

    order = 7

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_controller(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_controller(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.entity(context)

        controller = self.controller_name(context)

        service = self.service_name(context)

        validator = self.validator_name(context)

        framework_import = ImportResolver.framework(
            "base_controller",
            "BaseController",
        )

        service_import = ImportResolver.build(
            ModuleResolver.resolve(
                entity,
                "service",
            ),
            service,
        )

        validator_import = ImportResolver.build(
            ModuleResolver.resolve(
                entity,
                "validator",
            ),
            validator,
        )

        return f"""from sqlalchemy.orm import Session

{framework_import}
{service_import}
{validator_import}


class {controller}(BaseController):


    validator = {validator}


    def __init__(
        self,
        session: Session,
    ):

        super().__init__(
            {service}(
                session
            )
        )
"""
