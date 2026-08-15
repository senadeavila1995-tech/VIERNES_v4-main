class Naming:
    """
    Utilidades para nombres de clases, entidades y archivos.
    """

    @staticmethod
    def class_name(entity: str) -> str:
        """
        Convierte una entidad en nombre de clase.

        productos -> Producto
        usuarios -> Usuario
        factura -> Factura
        """

        entity = entity.lower()

        if entity.endswith("s"):

            entity = entity[:-1]

        return entity.capitalize()

    @staticmethod
    def variable_name(entity: str) -> str:
        """
        Nombre para variables.

        Producto -> producto
        """

        return entity[:1].lower() + entity[1:]

    @staticmethod
    def module_name(entity: str) -> str:
        """
        Nombre para módulos.

        Producto -> producto
        """

        return entity.lower()
