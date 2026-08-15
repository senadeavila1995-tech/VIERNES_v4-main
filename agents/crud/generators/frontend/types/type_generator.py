from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class TypeGenerator(BaseFrontendGenerator):

    name = "type"

    description = "Genera interfaces TypeScript."

    order = 50

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        class_name = self.type_name(context)

        fields = []

        for field in context.fields:

            ts_type = self.ts_type(field)

            fields.append(f"    {field.name}: {ts_type};")

        body = "\n".join(fields)

        return f"""
export interface {class_name} {{

{body}

}}
"""
