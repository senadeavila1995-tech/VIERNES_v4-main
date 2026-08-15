from agents.crud.generators.frontend.types.entity_type_generator import (
    EntityTypeGenerator,
)
from agents.crud.generators.frontend.types.create_type_generator import (
    CreateTypeGenerator,
)
from agents.crud.generators.frontend.types.update_type_generator import (
    UpdateTypeGenerator,
)
from agents.crud.generators.frontend.types.response_type_generator import (
    ResponseTypeGenerator,
)
from agents.crud.generators.frontend.types.filter_type_generator import (
    FilterTypeGenerator,
)
from agents.crud.generators.frontend.types.index_type_generator import (
    IndexTypeGenerator,
)

from agents.crud.generators.frontend.api.api_generator import ApiGenerator
from agents.crud.generators.frontend.api.service_generator import ServiceGenerator

from agents.crud.generators.frontend.hooks.hook_generator import HookGenerator

from agents.crud.generators.frontend.components.table_generator import TableGenerator
from agents.crud.generators.frontend.components.form_generator import FormGenerator
from agents.crud.generators.frontend.components.modal_generator import ModalGenerator
from agents.crud.generators.frontend.components.toolbar_generator import (
    ToolbarGenerator,
)
from agents.crud.generators.frontend.components.filter_generator import FilterGenerator

from agents.crud.generators.frontend.pages.page_generator import PageGenerator
from agents.crud.generators.frontend.routes.route_generator import RouteGenerator
from agents.crud.generators.frontend.index.index_generator import IndexGenerator


class FrontendModuleGenerator:
    """
    Orquestador principal del frontend.

    No genera archivos directamente.

    Ejecuta todos los generadores
    necesarios para construir
    un módulo React + TypeScript.
    """

    name = "frontend"

    description = "Frontend Module"

    order = 100

    def validate(self, context):

        return True

    def generate(self, context):

        files = []

        generators = [
            # =====================
            # TYPES
            # =====================
            EntityTypeGenerator(),
            CreateTypeGenerator(),
            UpdateTypeGenerator(),
            ResponseTypeGenerator(),
            FilterTypeGenerator(),
            IndexTypeGenerator(),
            # =====================
            # API
            # =====================
            ApiGenerator(),
            ServiceGenerator(),
            # =====================
            # HOOKS
            # =====================
            HookGenerator(),
            # =====================
            # COMPONENTS
            # =====================
            TableGenerator(),
            FormGenerator(),
            ModalGenerator(),
            ToolbarGenerator(),
            FilterGenerator(),
            # =====================
            # PAGE
            # =====================
            PageGenerator(),
            # =====================
            # ROUTES
            # =====================
            RouteGenerator(),
            # =====================
            # INDEX
            # =====================
            IndexGenerator(),
        ]

        for generator in generators:

            try:

                generated = generator.generate(context)

                if generated is None:
                    continue

                if isinstance(generated, list):

                    files.extend(generated)

                else:

                    files.append(generated)

            except Exception as e:

                print(f"[Frontend] {generator.name}: {e}")

        return files
