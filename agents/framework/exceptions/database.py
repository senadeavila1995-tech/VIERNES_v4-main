class DatabaseIntegrityError(Exception):
    """
    Error de integridad de base de datos.

    Se utiliza para desacoplar SQLAlchemy/FastAPI.

    La capa Database captura errores de integridad
    y los transforma en esta excepción de dominio.
    """

    def __init__(
        self,
        message: str = "Violación de integridad de base de datos.",
        original: Exception | None = None,
    ):
        super().__init__(message)

        self.message = message
        self.original = original
