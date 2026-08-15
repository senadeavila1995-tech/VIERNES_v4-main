class TypeMapper:
    """
    Convierte tipos CRUD genéricos a tipos Python
    y tipos SQLAlchemy.

    El modelo CRUD utiliza tipos independientes
    del motor de base de datos.
    """

    PYTHON_TYPES = {
        "int": "int",
        "integer": "int",
        "smallint": "int",
        "bigint": "int",

        "float": "float",
        "double": "float",
        "real": "float",
        "decimal": "float",

        "str": "str",
        "string": "str",
        "varchar": "str",
        "char": "str",
        "text": "str",

        "bool": "bool",
        "boolean": "bool",

        "date": "date",
        "datetime": "datetime",
        "timestamp": "datetime",
        "time": "time",

        "json": "dict",
        "uuid": "str",
        "enum": "str",
    }

    SQLALCHEMY_TYPES = {
        "int": "Integer",
        "integer": "Integer",
        "smallint": "SmallInteger",
        "bigint": "BigInteger",

        "float": "Float",
        "double": "Double",
        "real": "Float",
        "decimal": "Numeric",

        "str": "String",
        "string": "String",
        "varchar": "String",
        "char": "String",
        "text": "Text",

        "bool": "Boolean",
        "boolean": "Boolean",

        "date": "Date",
        "datetime": "DateTime",
        "timestamp": "DateTime",
        "time": "Time",

        "json": "JSON",
        "uuid": "Uuid",
        "enum": "Enum",
    }

    @classmethod
    def normalize(cls, field_type: str) -> str:
        """
        Normaliza el tipo recibido.
        """

        if not isinstance(field_type, str):
            raise ValueError(
                f"El tipo debe ser texto: {field_type!r}"
            )

        return field_type.strip().lower()

    @classmethod
    def python(cls, field_type: str) -> str:
        """
        Devuelve el tipo Python correspondiente.
        """

        normalized = cls.normalize(field_type)

        return cls.PYTHON_TYPES.get(
            normalized,
            "str",
        )

    @classmethod
    def sqlalchemy(cls, field_type: str) -> str:
        """
        Devuelve el nombre del tipo SQLAlchemy.
        """

        normalized = cls.normalize(field_type)

        if normalized not in cls.SQLALCHEMY_TYPES:
            raise ValueError(
                f"Tipo SQLAlchemy no soportado: {field_type}"
            )

        return cls.SQLALCHEMY_TYPES[normalized]
