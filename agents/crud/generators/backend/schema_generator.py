from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.utils.type_mapper import TypeMapper


class SchemaGenerator(BaseGenerator):
    """
    Genera el esquema de validación de una entidad.

    Reglas:

    - Un campo marcado como required es obligatorio.
    - Una PK autoincremental NO es obligatoria al crear.
    - Un campo nullable puede aceptar None.
    """

    name = "schema"

    description = "Genera el esquema de validación."

    order = 3

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_schema(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_schema(
        self,
        context: GenerationContext,
    ) -> str:

        schema_fields = []

        for field in context.fields:

            python_type = TypeMapper.python(
                field.type
            )

            # --------------------------------------------------
            # Una PK autoincremental es generada por la BD.
            # Por tanto NO es obligatoria al crear.
            # --------------------------------------------------

            required = (
                field.required
                and not field.auto_increment
            )

            schema_fields.append(
                f'''    "{field.name}": {{
        "type": {python_type},
        "required": {required}
    }}'''
            )

        schema = ",\n\n".join(
            schema_fields
        )

        return f'''"""
Schema generado automáticamente por VIERNES.

Entidad:
{context.entity_name}

No modificar manualmente.
"""


SCHEMA = {{

{schema}

}}
'''
