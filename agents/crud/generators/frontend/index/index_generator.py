from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class IndexGenerator(BaseFrontendGenerator):
    """
    Genera el punto de entrada del módulo frontend.
    """

    name = "frontend_index"

    description = "Genera índice del módulo frontend."

    order = 120

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        module = self.snake_name(context)
        entity = self.pascal_name(context)

        page = self.page_name(context)
        hook = self.hook_name(context)
        routes = self.camel_name(context)

        return f'''export type {{
    {entity},
    {entity}Create,
    {entity}Update,
    {entity}Response,
    {entity}Filter,
}} from "./types";

export {{ default as {page} }} from "./pages/{page}";

export {{ default as {entity}Table }} from "./components/{module}Table";

export {{ default as {entity}Form }} from "./components/{module}Form";

export {{ default as {entity}Modal }} from "./components/{module}Modal";

export {{ default as {entity}Toolbar }} from "./components/{module}Toolbar";

export {{ default as {entity}FilterComponent }} from "./components/{module}Filter";

export {{ {hook} }} from "./hooks/{hook}";

export {{ {routes}Routes }} from "./routes";
'''

    def folder(self) -> str:
        return ""

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "index.ts"
