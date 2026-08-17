from sqlalchemy import inspect

from agents.framework.database.connection import engine


class SchemaIntrospector:
    """
    Lee la estructura real de la base de datos.

    Convierte tablas existentes en información
    usable por el motor CRUD.
    """

    def __init__(self):
        self.inspector = inspect(engine)


    def table_exists(
        self,
        table_name: str,
    ) -> bool:

        return table_name in self.inspector.get_table_names()


    def get_columns(
        self,
        table_name: str,
    ) -> list[dict]:

        if not self.table_exists(table_name):
            return []

        return self.inspector.get_columns(
            table_name
        )


    def get_foreign_keys(
        self,
        table_name: str,
    ) -> list[dict]:

        if not self.table_exists(table_name):
            return []

        return self.inspector.get_foreign_keys(
            table_name
        )


    def inspect_table(
        self,
        table_name: str,
    ) -> dict:

        return {
            "table": table_name,
            "exists": self.table_exists(table_name),
            "columns": self.get_columns(table_name),
            "foreign_keys": self.get_foreign_keys(table_name),
        }
