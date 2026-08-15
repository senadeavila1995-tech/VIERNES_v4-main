from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class CreateTypeGenerator(BaseFrontendGenerator):
    """
    Genera el tipo utilizado para crear una entidad.
    """

    name = "create_type"

    description = "Genera el tipo TypeScript para creación."

    order = 2

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.type_name(context)

        fields = []

        for field in context.fields:

            if field.name == "id":
                continue

            fields.append(
                f"    {field.name}: {self.ts_type(field)};"
            )

        body = "\n".join(fields)

        return f"""export interface {entity}Create {{

{body}

}}
"""

    def folder(self) -> str:

        return "types"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}_create.ts"
