from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.utils.type_mapper import TypeMapper


class UpdateDtoGenerator(BaseGenerator):
    """
    Genera el DTO utilizado para actualización.
    """

    name = "dto_update"

    description = "Genera DTO Pydantic de actualización."

    order = 5


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
            "dto_update",
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


            fields.append(
                f"    {field.name}: {python_type} | None = None"
            )


        body = "\n\n".join(fields)


        return f'''"""
DTO Update generado automáticamente por VIERNES.

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

        return f"{self.snake_name(context)}_update.py"
