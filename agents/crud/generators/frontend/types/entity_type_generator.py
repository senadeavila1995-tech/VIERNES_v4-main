from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)
from agents.crud.models.generation_context import GenerationContext


class EntityTypeGenerator(BaseFrontendGenerator):
    """
    Genera el tipo principal de la entidad.

    Ejemplo:

    export interface Categoria {
        id: number;
        nombre: string;
    }
    """

    name = "entity_type"

    description = "Genera el tipo principal TypeScript."

    order = 1

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        interface_name = self.type_name(context)

        fields = []

        # ==========================================================
        # PRIMARY KEY IMPLÍCITA
        #
        # El backend genera automáticamente un id cuando la
        # definición no declara una clave primaria explícita.
        #
        # Las entidades Response/Entity deben reflejar ese id.
        # ==========================================================

        has_primary_key = any(
            getattr(field, "primary_key", False)
            for field in context.fields
        )

        if not has_primary_key:
            fields.append(
                "    id: number;"
            )

        for field in context.fields:
            fields.append(
                f"    {field.name}: {self.ts_type(field)};"
            )

        body = "\n".join(fields)

        return f'''/**
 * Archivo generado automáticamente por VIERNES.
 * No modificar manualmente.
 */

export interface {interface_name} {{

{body}

}}
'''

    def folder(self) -> str:
        return "types"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}.ts"
