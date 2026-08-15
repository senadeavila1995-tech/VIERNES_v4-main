from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class ResponseTypeGenerator(BaseFrontendGenerator):
    """
    Genera el tipo de respuesta de la API.
    """

    name = "response_type"

    description = "Genera el tipo TypeScript de respuesta."

    order = 4

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.type_name(context)
        snake_name = self.snake_name(context)

        return f'''import type {{ {entity} }} from "./{snake_name}";

export type {entity}Response = {entity};
'''

    def folder(self) -> str:
        return "types"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}_response.ts"
