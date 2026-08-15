import re
import unicodedata

from agents.crud.config.crud_structure import CRUD_STRUCTURE


class NamingResolver:
    """
    Responsable de construir todos los nombres utilizados por el
    motor CRUD.

    Toda la configuración se obtiene desde CRUD_STRUCTURE.
    """

    # ==========================================================
    # Normalización
    # ==========================================================

    @staticmethod
    def normalize(name: str) -> str:
        """
        Normaliza un nombre eliminando:

        - Tildes
        - Ñ -> N
        - Espacios repetidos
        - Caracteres especiales

        Ejemplos:

            Categoría
                -> Categoria

            Información Cliente
                -> Informacion Cliente

            Año Fiscal
                -> Anio Fiscal
        """

        name = name.strip()

        # Eliminar acentos
        name = unicodedata.normalize("NFD", name)
        name = "".join(c for c in name if unicodedata.category(c) != "Mn")

        # Eliminar caracteres especiales
        name = re.sub(r"[^A-Za-z0-9 ]+", "", name)

        # Espacios múltiples
        name = re.sub(r"\s+", " ", name)

        return name

    # ==========================================================
    # Conversión de nombres
    # ==========================================================

    
    @classmethod
    def snake(cls, name: str) -> str:
        """
        Convierte cualquier nombre a snake_case.

        Ejemplos:

            Mi Producto
                -> mi_producto

            DetalleProducto
                -> detalle_producto

            detalleProducto
                -> detalle_producto

            detalle_producto
                -> detalle_producto
        """

        name = name.strip()

        # Los separadores explícitos deben conservarse
        # como separadores de palabras.
        name = re.sub(
            r"[_-]+",
            " ",
            name,
        )

        # Normalizar tildes y caracteres especiales.
        name = cls.normalize(name)

        # Separar CamelCase / PascalCase.
        name = re.sub(
            r"(?<=[a-z0-9])(?=[A-Z])",
            " ",
            name,
        )

        # Convertir espacios a "_".
        name = re.sub(
            r"\s+",
            "_",
            name.strip(),
        )

        return name.lower()
    @classmethod
    def pascal(cls, name: str) -> str:
        """
        Convierte nombres a PascalCase.

        Ejemplos:

            mi_producto
                ↓
            MiProducto

            DetalleProducto
                ↓
            DetalleProducto

            detalle_producto
                ↓
            DetalleProducto

            Mi Producto
                ↓
            MiProducto
        """

        # Primero convertir separadores explícitos en espacios
        name = re.sub(
            r"[_-]+",
            " ",
            name.strip(),
        )

        # Normalizar después de preservar los separadores
        name = cls.normalize(name)

        # Separar CamelCase / PascalCase
        name = re.sub(
            r"(?<=[a-z0-9])(?=[A-Z])",
            " ",
            name,
        )

        return "".join(
            word[:1].upper() + word[1:]
            for word in name.split()
        )

    @classmethod
    def camel(cls, name: str) -> str:
        """
        mi_producto

        ↓

        miProducto
        """

        pascal = cls.pascal(name)

        return pascal[:1].lower() + pascal[1:]

    # ==========================================================
    # Configuración CRUD
    # ==========================================================

    @staticmethod
    def config(kind: str) -> dict:

        config = CRUD_STRUCTURE.crud_types.get(kind)

        if config is None:
            raise ValueError(f"Tipo CRUD desconocido: {kind}")

        return config

    # ==========================================================
    # Nombre de archivo
    # ==========================================================

    @classmethod
    def filename(
        cls,
        entity: str,
        kind: str,
    ) -> str:
        """
        Construye el nombre del archivo.
        """

        suffix = cls.config(kind)["file_suffix"]

        if kind == "page":
            return cls.pascal(entity) + suffix

        return cls.snake(entity) + suffix

    # ==========================================================
    # Nombre de clase
    # ==========================================================

    @classmethod
    def class_name(
        cls,
        entity: str,
        kind: str = "model",
    ) -> str:

        suffix = cls.config(kind)["class_suffix"]

        return cls.pascal(entity) + suffix

    # ==========================================================
    # Información
    # ==========================================================

    @classmethod
    def info(
        cls,
        kind: str,
    ) -> dict:

        return cls.config(kind)

    @staticmethod
    def plural(value: str) -> str:
        """
        Convierte un nombre singular en plural básico
        para nombres de relaciones ORM.
        """

        if value.endswith("s"):
            return value

        if value.endswith("y"):
            return value[:-1] + "ies"

        return value + "s"

