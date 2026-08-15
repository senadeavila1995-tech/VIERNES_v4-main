from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.utils.type_mapper import TypeMapper
from agents.crud.resolvers.module_resolver import ModuleResolver


class ResponseDtoGenerator(BaseGenerator):
    """
    Genera DTO Pydantic de respuesta.

    Las relaciones many_to_one se representan como DTO anidado.

    Las relaciones one_to_many y many_to_many no se expanden
    automáticamente para evitar ciclos de serialización Pydantic
    producidos por relaciones ORM bidireccionales.
    """

    name = "dto_response"

    description = "Genera DTO Pydantic de respuesta."

    order = 6

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
            "dto_response",
        )

        fields = []

        relationship_imports = []

        # ==================================
        # Campos normales
        # ==================================

        for field in context.fields:

            python_type = TypeMapper.python(
                field.type
            )

            annotation = python_type

            if field.nullable or not field.required:
                annotation = f"{python_type} | None"

            fields.append(
                f"    {field.name}: {annotation}"
            )

        # ==================================
        # Relaciones
        # ==================================
        #
        # Solamente expandimos relaciones
        # many_to_one.
        #
        # Las relaciones one_to_many y
        # many_to_many se omiten del DTO
        # para evitar ciclos:
        #
        # ClienteResponse
        #     -> OrdenCompraResponse
        #         -> ClienteResponse
        #
        # y:
        #
        # OrdenCompraResponse
        #     -> LineaPedidoResponse
        #         -> OrdenCompraResponse
        #
        # Las relaciones ORM permanecen intactas.
        # ==================================

        for relation in context.definition.relationships:

            if relation.relation_type != "many_to_one":
                continue

            response_class = (
                f"{relation.target}Response"
            )

            relationship_imports.append(
                (
                    ModuleResolver.dto_response(
                        relation.target
                    ),
                    response_class,
                )
            )

            fields.append(
                f'    {relation.name}: "{response_class} | None" = None'
            )

        # ==================================
        # Imports TYPE_CHECKING
        # ==================================

        imports = ""

        if relationship_imports:

            imports = (
                "\nif TYPE_CHECKING:\n"
            )

            for module, target in sorted(
                set(relationship_imports)
            ):

                imports += (
                    f"    from {module} import {target}\n"
                )

        body = "\n\n".join(fields)

        return f'''"""
DTO Response generado automáticamente por VIERNES.

Entidad:
{context.entity_name}
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel
{imports}


class {class_name}(BaseModel):

{body}

    class Config:
        from_attributes = True
'''

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}_response.py"
