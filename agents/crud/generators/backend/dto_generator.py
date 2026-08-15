from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.naming_resolver import NamingResolver
from agents.crud.utils.type_mapper import TypeMapper


class DtoGenerator(BaseGenerator):
    """
    Genera los DTO Pydantic de una entidad.

    Los DTO representan el contrato de datos utilizado
    por FastAPI.

    Se generan:

        ProductoDTO

    utilizando los campos definidos en CrudField.
    """

    name = "dto"

    description = "Genera el DTO Pydantic."

    order = 3

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_dto(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_dto(
        self,
        context: GenerationContext,
    ) -> str:

        class_name = self.dto_name(context)

        fields = []

        for field in context.fields:

            python_type = TypeMapper.python(
                field.type
            )

            annotation = python_type

            if field.nullable:

                annotation = f"{python_type} | None"

            if not field.required:

                annotation = f"{python_type} | None"

            default = "..."

            if field.default is not None:

                default = repr(field.default)

            elif not field.required or field.nullable:

                default = "None"

            fields.append(
                f"    {field.name}: {annotation} = {default}"
            )

        fields_text = "\n\n".join(fields)

        return f'''"""
DTO generado automáticamente por VIERNES.

Entidad:
{context.entity_name}

Utilizado como contrato de datos para FastAPI/Pydantic.
"""

from pydantic import BaseModel


class {class_name}(BaseModel):

{fields_text}
'''
