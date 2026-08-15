from agents.crud.models.crud_field import CrudField


class TypeResolver:
    """
    Convierte los tipos genéricos del motor CRUD
    al tipo específico del motor de base de datos.

    Ejemplo:

        string
            ↓
        MySQL
            ↓
        VARCHAR(255)

        decimal
            ↓
        PostgreSQL
            ↓
        NUMERIC(10,2)

    También acepta alias comunes:

        int  → integer
        str  → string
        bool → boolean
        numeric → decimal
    """

    # ==========================================================
    # Motores soportados
    # ==========================================================

    MYSQL = {
        "string": "VARCHAR",
        "text": "TEXT",
        "integer": "INT",
        "bigint": "BIGINT",
        "float": "FLOAT",
        "double": "DOUBLE",
        "decimal": "DECIMAL",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "DATETIME",
        "time": "TIME",
        "timestamp": "TIMESTAMP",
        "json": "JSON",
        "uuid": "CHAR(36)",
        "enum": "ENUM",
    }

    POSTGRESQL = {
        "string": "VARCHAR",
        "text": "TEXT",
        "integer": "INTEGER",
        "bigint": "BIGINT",
        "float": "REAL",
        "double": "DOUBLE PRECISION",
        "decimal": "NUMERIC",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "TIMESTAMP",
        "time": "TIME",
        "timestamp": "TIMESTAMP",
        "json": "JSONB",
        "uuid": "UUID",
        "enum": "TEXT",
    }

    SQLITE = {
        "string": "TEXT",
        "text": "TEXT",
        "integer": "INTEGER",
        "bigint": "INTEGER",
        "float": "REAL",
        "double": "REAL",
        "decimal": "REAL",
        "boolean": "INTEGER",
        "date": "TEXT",
        "datetime": "TEXT",
        "time": "TEXT",
        "timestamp": "TEXT",
        "json": "TEXT",
        "uuid": "TEXT",
        "enum": "TEXT",
    }

    SQLSERVER = {
        "string": "NVARCHAR",
        "text": "NVARCHAR(MAX)",
        "integer": "INT",
        "bigint": "BIGINT",
        "float": "FLOAT",
        "double": "FLOAT",
        "decimal": "DECIMAL",
        "boolean": "BIT",
        "date": "DATE",
        "datetime": "DATETIME2",
        "time": "TIME",
        "timestamp": "DATETIME2",
        "json": "NVARCHAR(MAX)",
        "uuid": "UNIQUEIDENTIFIER",
        "enum": "NVARCHAR",
    }

    # ==========================================================
    # Registro de motores
    # ==========================================================

    ENGINES = {
        "mysql": MYSQL,
        "postgresql": POSTGRESQL,
        "sqlite": SQLITE,
        "sqlserver": SQLSERVER,
    }

    # ==========================================================
    # Alias de tipos
    # ==========================================================

    TYPE_ALIASES = {
        # Texto
        "str": "string",
        "string": "string",
        "varchar": "string",
        "char": "string",

        # Enteros
        "int": "integer",
        "integer": "integer",
        "smallint": "integer",

        # Enteros grandes
        "long": "bigint",
        "bigint": "bigint",

        # Flotantes
        "float": "float",
        "double": "double",

        # Decimales
        "decimal": "decimal",
        "numeric": "decimal",

        # Booleanos
        "bool": "boolean",
        "boolean": "boolean",

        # Fechas
        "date": "date",
        "datetime": "datetime",
        "time": "time",
        "timestamp": "timestamp",

        # Otros
        "text": "text",
        "json": "json",
        "uuid": "uuid",
        "enum": "enum",
    }

    # ==========================================================
    # Normalización
    # ==========================================================

    @classmethod
    def normalize_type(
        cls,
        field_type: str,
    ) -> str:
        """
        Normaliza los alias de tipos del motor CRUD.

        Ejemplos:

            int
                ↓
            integer

            str
                ↓
            string

            bool
                ↓
            boolean

            numeric
                ↓
            decimal
        """

        if not isinstance(field_type, str):

            raise ValueError(
                f"El tipo debe ser texto: {field_type!r}"
            )

        field_type = field_type.strip().lower()

        if not field_type:

            raise ValueError(
                "El tipo del campo no puede estar vacío."
            )

        return cls.TYPE_ALIASES.get(
            field_type,
            field_type,
        )

    # ==========================================================
    # API pública
    # ==========================================================

    @classmethod
    def resolve(
        cls,
        field: CrudField,
        engine: str,
    ) -> str:
        """
        Devuelve el tipo SQL correspondiente
        para un campo y un motor específico.
        """

        engine = engine.lower()

        if engine not in cls.ENGINES:

            raise ValueError(
                f"Motor no soportado: {engine}"
            )

        mapping = cls.ENGINES[engine]

        normalized_type = cls.normalize_type(
            field.type
        )

        if normalized_type not in mapping:

            raise ValueError(
                f"Tipo no soportado: {field.type}"
            )

        sql_type = mapping[normalized_type]

        return cls._decorate(
            sql_type=sql_type,
            field=field,
            engine=engine,
            field_type=normalized_type,
        )

    # ==========================================================
    # Decoradores de tipos
    # ==========================================================

    @classmethod
    def _decorate(
        cls,
        sql_type: str,
        field: CrudField,
        engine: str,
        field_type: str,
    ) -> str:
        """
        Añade longitud, precisión,
        escala o ENUM según el tipo.
        """

        # ======================================================
        # VARCHAR(...)
        # ======================================================

        if field_type == "string":

            length = field.length or 255

            return f"{sql_type}({length})"

        # ======================================================
        # DECIMAL(...)
        # ======================================================

        if field_type == "decimal":

            precision = field.precision or 10

            scale = field.scale or 2

            return f"{sql_type}({precision},{scale})"

        # ======================================================
        # ENUM(...)
        # ======================================================

        if field_type == "enum":

            if engine == "mysql":

                values = ",".join(
                    f"'{value}'"
                    for value in (field.enum or [])
                )

                return f"ENUM({values})"

            return sql_type

        return sql_type

    # ==========================================================
    # Utilidades
    # ==========================================================

    @classmethod
    def supported_engines(cls) -> list[str]:
        """
        Devuelve la lista de motores soportados.
        """

        return list(cls.ENGINES.keys())

    @classmethod
    def supported_types(
        cls,
        engine: str,
    ) -> list[str]:
        """
        Devuelve los tipos canónicos soportados
        para un motor específico.
        """

        engine = engine.lower()

        if engine not in cls.ENGINES:

            raise ValueError(
                f"Motor no soportado: {engine}"
            )

        return list(cls.ENGINES[engine].keys())

    @classmethod
    def supported_aliases(cls) -> list[str]:
        """
        Devuelve todos los alias aceptados
        por el motor CRUD.
        """

        return list(cls.TYPE_ALIASES.keys())