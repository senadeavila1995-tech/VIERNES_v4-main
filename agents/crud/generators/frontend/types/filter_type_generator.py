from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class FilterTypeGenerator(BaseFrontendGenerator):
    """
    Genera el tipo utilizado para filtros del listado.
    """

    name = "filter_type"

    description = "Genera el tipo TypeScript para filtros."

    order = 5

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.type_name(context)

        fields = []

        for field in context.fields:

            fields.append(
                f"    {field.name}?: {self.ts_type(field)};"
            )

        body = "\n".join(fields)

        return f"""export interface {entity}Filter {{

{body}

}}
"""

    def folder(self) -> str:

        return "types"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}_filter.ts"
