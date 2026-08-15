from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.type_resolver import TypeResolver
from agents.crud.resolvers.naming_resolver import NamingResolver


class SqlGenerator(BaseGenerator):
    """
    Genera el script SQL de creación de tablas.

    Soporta:

    - PRIMARY KEY
    - AUTO_INCREMENT
    - UNIQUE
    - NOT NULL
    - DEFAULT
    - FOREIGN KEY
    - INDEX
    - TIMESTAMPS
    - SOFT DELETE
    """

    name = "sql"

    description = "Genera el script SQL."

    order = 9

    # ==========================================================
    # API
    # ==========================================================

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        return self._build_create_table(context)

    # ==========================================================
    # CREATE TABLE
    # ==========================================================

    def _build_create_table(
        self,
        context: GenerationContext,
    ) -> str:

        table = context.table_name

        columns = self._build_columns(context)

        constraints = self._build_constraints(context)

        body = columns

        if constraints:

            body += ",\n\n" + constraints

        return f"""CREATE TABLE {table} (

{body}

);
"""

    # ==========================================================
    # Columnas
    # ==========================================================

    def _build_columns(
        self,
        context: GenerationContext,
    ) -> str:

        columns = []

        for field in context.fields:

            columns.append(
                self._build_column(
                    field,
                    context.project.database,
                )
            )

        # ======================================================
        # Timestamps
        # ======================================================

        if context.definition.timestamps:

            columns.append(
                self._build_created_at(
                    context.project.database
                )
            )

            columns.append(
                self._build_updated_at(
                    context.project.database
                )
            )

        # ======================================================
        # Soft Delete
        # ======================================================

        if context.definition.soft_delete:

            columns.append(
                "deleted_at TIMESTAMP NULL"
            )

        return ",\n".join(columns)

    # ==========================================================
    # Columna individual
    # ==========================================================

    def _build_column(
        self,
        field,
        engine,
    ) -> str:

        sql = f"{field.name} "

        sql += TypeResolver.resolve(
            field,
            engine,
        )

        if field.primary_key:

            sql += " PRIMARY KEY"

        if field.auto_increment:

            if engine == "mysql":

                sql += " AUTO_INCREMENT"

        if field.required and not field.nullable:

            sql += " NOT NULL"

        if field.unique:

            sql += " UNIQUE"

        if field.default is not None:

            sql += f" DEFAULT {field.default}"

        return sql

    # ==========================================================
    # Timestamp created_at
    # ==========================================================

    def _build_created_at(
        self,
        engine,
    ) -> str:

        if engine == "mysql":

            return (
                "created_at TIMESTAMP "
                "NOT NULL "
                "DEFAULT CURRENT_TIMESTAMP"
            )

        return (
            "created_at TIMESTAMP "
            "NOT NULL"
        )

    # ==========================================================
    # Timestamp updated_at
    # ==========================================================

    def _build_updated_at(
        self,
        engine,
    ) -> str:

        if engine == "mysql":

            return (
                "updated_at TIMESTAMP "
                "NOT NULL "
                "DEFAULT CURRENT_TIMESTAMP "
                "ON UPDATE CURRENT_TIMESTAMP"
            )

        return (
            "updated_at TIMESTAMP "
            "NOT NULL"
        )

    # ==========================================================
    # Restricciones
    # ==========================================================

    def _build_constraints(
        self,
        context: GenerationContext,
    ) -> str:

        constraints = []

        constraints.extend(
            self._build_foreign_keys(context)
        )

        constraints.extend(
            self._build_indexes(context)
        )

        return ",\n".join(constraints)

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    def _build_foreign_keys(
        self,
        context: GenerationContext,
    ) -> list[str]:

        constraints = []

        for field in context.definition.foreign_keys:

            reference_table = NamingResolver.snake(
                field.references
            )

            fk = (
                f"CONSTRAINT fk_{context.table_name}_{field.name} "
                f"FOREIGN KEY ({field.name}) "
                f"REFERENCES {reference_table}"
                f"({field.references_field})"
            )

            if field.on_delete:

                fk += (
                    f" ON DELETE {field.on_delete}"
                )

            if field.on_update:

                fk += (
                    f" ON UPDATE {field.on_update}"
                )

            constraints.append(fk)

        return constraints

    # ==========================================================
    # Índices
    # ==========================================================

    def _build_indexes(
        self,
        context: GenerationContext,
    ) -> list[str]:

        indexes = []

        for field in context.definition.indexed_fields:

            indexes.append(
                f"INDEX idx_{field.name} "
                f"({field.name})"
            )

        return indexes
