from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.utils.type_mapper import TypeMapper


class CreateDtoGenerator(BaseGenerator):
    """
    Genera el DTO utilizado para creación.

    Excluye campos generados por la base de datos.
    """

    name = "dto_create"

    description = "Genera DTO Pydantic de creación."

    order = 4


    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_dto(context)


    def _build_dto(
        self,
        context: GenerationContext,
    ) -> str:

        class_name = self.class_name(
            context,
            "dto_create",
        )

        fields = []

        for field in context.fields:

            if field.name in (
                "id",
                "created_at",
                "updated_at",
                "deleted_at",
            ):
                continue

            python_type = TypeMapper.python(
                field.type
            )

            annotation = python_type

            if field.nullable or not field.required:
                annotation = f"{python_type} | None"

            default = "..."

            if field.default is not None:
                default = repr(field.default)

            elif field.nullable or not field.required:
                default = "None"

            fields.append(
                f"    {field.name}: {annotation} = {default}"
            )

        body = "\n\n".join(fields)

        return f'''"""
DTO Create generado automáticamente por VIERNES.

Entidad:
{context.entity_name}
"""

from pydantic import BaseModel


class {class_name}(BaseModel):

{body}
'''


    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}_create.py"
