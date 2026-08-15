from agents.crud.config.crud_structure import CRUD_STRUCTURE
from agents.crud.resolvers.naming_resolver import NamingResolver


class ModuleResolver:
    """
    Responsable de construir los módulos Python
    utilizados por los imports.

    No conoce rutas físicas.
    Únicamente construye módulos.
    """

    @staticmethod
    def exists(kind: str) -> bool:
        return kind in CRUD_STRUCTURE.crud_types

    @classmethod
    def config(cls, kind: str) -> dict:

        if not cls.exists(kind):
            raise ValueError(f"Tipo CRUD desconocido: {kind}")

        return CRUD_STRUCTURE.crud_types[kind]

    @classmethod
    def resolve(
        cls,
        entity: str,
        kind: str,
    ) -> str:

        entity = NamingResolver.snake(entity)

        config = cls.config(kind)

        folder = config["folder"]
        suffix = config["module_suffix"]

        if suffix is None:
            return f"..{folder}.{entity}"

        return f"..{folder}.{entity}_{suffix}"

    @classmethod
    def controller(cls, entity: str):
        return cls.resolve(entity, "controller")

    @classmethod
    def service(cls, entity: str):
        return cls.resolve(entity, "service")

    @classmethod
    def repository(cls, entity: str):
        return cls.resolve(entity, "repository")

    @classmethod
    def validator(cls, entity: str):
        return cls.resolve(entity, "validator")

    @classmethod
    def schema(cls, entity: str):
        return cls.resolve(entity, "schema")

    @classmethod
    def dto(cls, entity: str):
        return cls.resolve(entity, "dto")

    @classmethod
    def dto_create(cls, entity: str):
        return cls.resolve(entity, "dto_create")

    @classmethod
    def dto_update(cls, entity: str):
        return cls.resolve(entity, "dto_update")

    @classmethod
    def dto_response(cls, entity: str):
        return cls.resolve(entity, "dto_response")

    @classmethod
    def model(cls, entity: str):
        return cls.resolve(entity, "model")

    @classmethod
    def route(cls, entity: str):
        return cls.resolve(entity, "route")

    @classmethod
    def database(cls, entity: str):
        return cls.resolve(entity, "database")

    @classmethod
    def view(cls, entity: str):
        return cls.resolve(entity, "view")
