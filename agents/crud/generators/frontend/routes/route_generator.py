from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class RouteGenerator(BaseFrontendGenerator):
    """
    Genera las rutas React del módulo.
    """

    name = "frontend_route"

    description = "Genera rutas React del módulo."

    order = 110

    def generate(
        self,
        context: GenerationContext,
    ):

        if not self.validate(context):
            raise ValueError(
                f"El generador '{self.name}' no puede ejecutarse."
            )

        return self.build_file(
            entity=context.entity_name,
            folder="",
            filename=self.filename(context),
            content=self.generate_content(context),
            description=self.description,
        )


    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        page = self.page_name(context)
        module = self.snake_name(context)
        route_name = self.camel_name(context)

        return f'''

import {page} from "./pages/{page}";

export const {route_name}Routes = [
    {{
        path: "/{module}",
        element: <{page} />,
    }},
];
'''

    def folder(self) -> str:
        return ""

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "routes.tsx"
