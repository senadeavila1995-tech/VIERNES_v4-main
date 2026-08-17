from agents.crud.validators.schema_introspector import SchemaIntrospector


class SchemaValidator:
    """
    Compara la definición CRUD contra
    el esquema real de la base de datos.
    """


    BASE_AUTO_FIELDS = {
        "created_at",
        "updated_at",
    }


    @staticmethod
    def compare(definition):

        result = {
            "table": definition.table,
            "exists": False,
            "missing_in_crud": [],
            "missing_in_database": [],
        }


        introspector = SchemaIntrospector()

        table_info = introspector.inspect_table(
            definition.table
        )


        if not table_info["exists"]:
            return result


        result["exists"] = True


        database_columns = {
            column["name"]
            for column in table_info["columns"]
        }


        crud_columns = {
            field.name
            for field in definition.fields
        }


        # Campos generados por VIERNES
        crud_columns.update(
            SchemaValidator.BASE_AUTO_FIELDS
        )


        # Soft delete solo si está activado
        if definition.soft_delete:
            crud_columns.add(
                "deleted_at"
            )


        result["missing_in_crud"] = sorted(
            database_columns - crud_columns
        )


        result["missing_in_database"] = sorted(
            crud_columns - database_columns
        )


        return result
