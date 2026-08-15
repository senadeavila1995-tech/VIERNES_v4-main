from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class IndexTypeGenerator(BaseFrontendGenerator):
    """
    Genera el índice de exports de los tipos TypeScript.
    """

    name = "index_type"

    description = "Genera índice de tipos TypeScript."

    order = 6

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        filename = self.snake_name(context)

        return f"""export type {{ {self.type_name(context)} }} from "./{filename}";

export type {{ {self.type_name(context)}Create }} from "./{filename}_create";

export type {{ {self.type_name(context)}Update }} from "./{filename}_update";

export type {{ {self.type_name(context)}Response }} from "./{filename}_response";

export type {{ {self.type_name(context)}Filter }} from "./{filename}_filter";
"""

    def folder(self) -> str:

        return "types"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "index.ts"
