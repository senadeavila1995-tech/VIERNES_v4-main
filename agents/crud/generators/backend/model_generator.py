from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.utils.type_mapper import TypeMapper
from agents.crud.resolvers.import_resolver import ImportResolver
from agents.crud.resolvers.naming_resolver import NamingResolver


class ModelGenerator(BaseGenerator):
    """
    Genera modelos SQLAlchemy declarativos.

    Responsabilidades:

    - Generar imports SQLAlchemy.
    - Generar la clase del modelo.
    - Generar columnas.
    - Generar claves primarias.
    - Generar Foreign Keys.
    - Generar restricciones básicas.
    - Generar timestamps.
    - Generar soft delete.
    """

    name = "model"

    description = "Genera el modelo SQLAlchemy."

    order = 2

    # ==========================================================
    # Generación
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_model(context)

    # ==========================================================
    # Construcción
    # ==========================================================

    def _build_model(
        self,
        context: GenerationContext,
    ) -> str:

        class_name = self.class_name(context)

        imports = self._build_imports(context)

        columns = []
        for field in context.fields:

            columns.append(
                self._build_column(
                    context,
                    field,
                )
            )

        # ======================================================
        # Timestamps
        # ======================================================

        if context.definition.timestamps:

            columns.append(
                self._build_created_at()
            )

            columns.append(
                self._build_updated_at()
            )

        # ======================================================
        # Soft Delete
        # ======================================================

        if context.definition.soft_delete:

            columns.append(
                self._build_deleted_at()
            )

        # ======================================================
        # Relationships ORM
        # ======================================================

        relationships = self._build_relationships(
            context
        )

        if relationships:
            columns.append(
                relationships
            )

        columns_text = "\n\n".join(columns)

        return f'''"""
Modelo generado automáticamente por VIERNES.

Entidad:
{context.entity_name}

Tabla:
{context.table_name}
"""

from __future__ import annotations

{imports}


class {class_name}(Base):

    __tablename__ = "{context.table_name}"

{columns_text}
'''

    # ==========================================================
    # Imports
    # ==========================================================

    def _build_imports(
        self,
        context: GenerationContext,
    ) -> str:

        datetime_types = set()

        for field in context.fields:
            if field.type == "date":
                datetime_types.add("date")
            elif field.type == "datetime":
                datetime_types.add("datetime")

        if context.definition.timestamps or context.definition.soft_delete:
            datetime_types.add("datetime")

        imports = []

        if datetime_types:
            imports.append(
                "from datetime import "
                + ", ".join(sorted(datetime_types))
            )

        imports.extend(
            [
                ImportResolver.framework(
                    "base_model",
                    "Base",
                ),
                "from sqlalchemy import ForeignKey",
                "from sqlalchemy.orm import Mapped, mapped_column, relationship",
            ]
        )

        sqlalchemy_types = set()

        for field in context.fields:

            if field.foreign_key:
                sqlalchemy_type = TypeMapper.sqlalchemy(
                    "integer"
                )
            else:
                sqlalchemy_type = TypeMapper.sqlalchemy(
                    field.type
                )

            sqlalchemy_types.add(
                sqlalchemy_type
            )

        # ======================================================
        # Timestamps / Soft Delete
        # ======================================================

        if context.definition.timestamps:
            sqlalchemy_types.add("DateTime")

        if context.definition.soft_delete:
            sqlalchemy_types.add("DateTime")

        ordered_types = [
            "Integer",
            "SmallInteger",
            "BigInteger",
            "Float",
            "Double",
            "Numeric",
            "String",
            "Text",
            "Boolean",
            "Date",
            "DateTime",
            "Time",
            "JSON",
            "Uuid",
            "Enum",
        ]

        selected_types = [
            type_name
            for type_name in ordered_types
            if type_name in sqlalchemy_types
        ]

        if selected_types:

            imports.insert(
                2,
                "from sqlalchemy import "
                + ", ".join(selected_types),
            )

        # ======================================================
        # SQLAlchemy func
        # ======================================================

        if (
            context.definition.timestamps
            or context.definition.soft_delete
        ):

            imports.insert(
                3,
                "from sqlalchemy.sql import func",
            )


        # ======================================================
        # Relationship TYPE_CHECKING imports
        # ======================================================

        if context.definition.relationships:

            imports.append(
                "from typing import TYPE_CHECKING"
            )

            imports.append(
                ""
            )

            imports.append(
                "if TYPE_CHECKING:"
            )

            relationship_imports = set()

            for relation in context.definition.relationships:

                relationship_import = (
                    f"    from ..{NamingResolver.snake(relation.target)}"
                    f".models.{NamingResolver.snake(relation.target)}"
                    f" import {NamingResolver.pascal(relation.target)}"
                )

                if relationship_import in relationship_imports:
                    continue

                relationship_imports.add(
                    relationship_import
                )

                imports.append(
                    relationship_import
                )


        return "\n".join(imports)

    # ==========================================================
    # Columna
    # ==========================================================


    # ==========================================================
    # Relationships ORM
    # ==========================================================

    def _build_relationships(
        self,
        context: GenerationContext,
    ) -> str:

        lines = []

        definition = context.definitions.get(
            context.definition.entity,
            context.definition,
        )

        relations = list(
            definition.relationships
        )

        definitions = getattr(
            context,
            "definitions",
            {}
        )

        for entity_name, definition in definitions.items():

            for relation in definition.relationships:

                if relation.target == context.definition.entity:

                    exists = any(
                        existing.name == relation.back_populates
                        for existing in relations
                    )

                    if relation.back_populates and not exists:

                        from agents.crud.models.crud_relationship import CrudRelationship

                        relations.append(
                            CrudRelationship(
                                name=relation.back_populates,
                                target=entity_name,
                                relation_type="one_to_many",
                                back_populates=relation.name,
                                foreign_key_field=relation.foreign_key_field,
                                on_delete=relation.on_delete,
                                lazy=relation.lazy,
                            )
                        )


        for relation in relations:


            args = [
                f'"{relation.target}"'
            ]

            if relation.back_populates:

                args.append(
                    f'back_populates="{relation.back_populates}"'
                )

            if relation.foreign_key_field:

                if relation.relation_type in (
                    "one_to_many",
                    "many_to_many",
                ):
                    foreign_key_owner = relation.target
                else:
                    foreign_key_owner = context.definition.entity

                args.append(
                    f'foreign_keys="{foreign_key_owner}.{relation.foreign_key_field}"'
                )

            if relation.lazy:

                args.append(
                    f'lazy="{relation.lazy}"'
                )

            # ==================================================
            # ON DELETE CASCADE
            # ==================================================
            #
            # passive_deletes=True debe aplicarse únicamente
            # al lado padre de la relación (colección).
            #
            # Esto permite que SQLAlchemy delegue el borrado
            # de los registros hijos a la FK de la base de datos.
            #
            # Ejemplo:
            #
            # Producto
            #   └── detalle_productos
            #          FK producto_id
            #          ON DELETE CASCADE
            #
            # Resultado:
            #
            # detalle_productos = relationship(
            #     ...,
            #     passive_deletes=True
            # )
            #
            # Para ON DELETE RESTRICT no se agrega nada.

            if (
                relation.relation_type in (
                    "one_to_many",
                    "many_to_many",
                )
                and relation.on_delete
                and relation.on_delete.upper() == "CASCADE"
            ):

                args.append(
                    "passive_deletes=True"
                )

            if relation.relation_type in (
                "one_to_many",
                "many_to_many",
            ):
                mapped_type = f'list["{relation.target}"]'
            else:
                mapped_type = f'"{relation.target}"'

            lines.append(
                f"    {relation.name}: Mapped[{mapped_type}] = relationship("
                + ", ".join(args)
                + ")"
            )

        return "\n\n".join(lines)


    def _build_column(
        self,
        context: GenerationContext,
        field,
    ) -> str:

        if field.foreign_key:
            sqlalchemy_type = TypeMapper.sqlalchemy(
                "integer"
            )
        else:
            sqlalchemy_type = TypeMapper.sqlalchemy(
                field.type
            )

        # ======================================================
        # Longitud de tipos String
        # ======================================================

        if sqlalchemy_type == "String":
            length = getattr(field, "length", None)

            if length:
                sqlalchemy_type = f"String({length})"
            else:
                sqlalchemy_type = "String(255)"

        arguments = [
            sqlalchemy_type,
        ]

        # ======================================================
        # Foreign Key
        # ======================================================

        if field.foreign_key:

            if not field.references:

                raise ValueError(
                    f"El campo '{field.name}' está marcado "
                    "como Foreign Key pero no tiene "
                    "'references'."
                )

            reference_table = NamingResolver.snake(
                field.references
            )

            # Resolver tabla real usando las definiciones disponibles
            for definition in context.definitions.values():

                if (
                    definition.entity == field.references
                    or NamingResolver.snake(definition.entity) == reference_table
                ):
                    reference_table = definition.table
                    break

            reference = (
                f"{reference_table}."
                f"{field.references_field}"
            )

            foreign_key_options = []

            if field.on_delete:

                foreign_key_options.append(
                    f'ondelete="{field.on_delete}"'
                )

            if field.on_update:

                foreign_key_options.append(
                    f'onupdate="{field.on_update}"'
                )

            foreign_key_text = ""

            if foreign_key_options:

                foreign_key_text = (
                    ", "
                    + ", ".join(foreign_key_options)
                )

            arguments.append(
                f'ForeignKey("{reference}"{foreign_key_text})'
            )

        # ======================================================
        # Parámetros
        # ======================================================

        options = []

        if field.primary_key:

            options.append(
                "primary_key=True"
            )

        if field.nullable:

            options.append(
                "nullable=True"
            )

        else:

            options.append(
                "nullable=False"
            )

        if field.unique:

            options.append(
                "unique=True"
            )

        if field.index:

            options.append(
                "index=True"
            )

        if field.auto_increment:

            options.append(
                "autoincrement=True"
            )

        if field.default is not None:

            options.append(
                f"default={self._format_default(field.default)}"
            )

        arguments_text = ", ".join(arguments)

        options_text = ""

        if options:

            options_text = ", " + ", ".join(options)

        return (
            f"    {field.name}: Mapped[{self._python_type(field.type)}] "
            f"= mapped_column("
            f"{arguments_text}"
            f"{options_text}"
            f")"
        )

    # ==========================================================
    # Timestamps
    # ==========================================================

    def _build_created_at(self) -> str:

        return (
            "    created_at: Mapped[datetime] = mapped_column(\n"
            "        DateTime,\n"
            "        nullable=False,\n"
            "        server_default=func.now(),\n"
            "    )"
        )

    def _build_updated_at(self) -> str:

        return (
            "    updated_at: Mapped[datetime] = mapped_column(\n"
            "        DateTime,\n"
            "        nullable=False,\n"
            "        server_default=func.now(),\n"
            "        onupdate=func.now(),\n"
            "    )"
        )

    # ==========================================================
    # Soft Delete
    # ==========================================================

    def _build_deleted_at(self) -> str:

        return (
            "    deleted_at: Mapped[datetime | None] = mapped_column(\n"
            "        DateTime,\n"
            "        nullable=True,\n"
            "    )"
        )

    # ==========================================================
    # Tipo Python
    # ==========================================================

    def _python_type(
        self,
        field_type: str,
    ) -> str:

        if field_type.lower() == "fk":
            field_type = "integer"

        return TypeMapper.python(
            field_type
        )

    # ==========================================================
    # Default
    # ==========================================================

    def _format_default(
        self,
        value,
    ) -> str:

        if isinstance(value, str):

            lowered = value.lower()

            if lowered in {
                "true",
                "false",
                "none",
            }:

                return lowered

            return repr(value)

        return repr(value)
