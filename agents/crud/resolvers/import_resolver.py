class ImportResolver:
    """
    Responsable de construir las sentencias import utilizadas
    por el motor CRUD.

    Toda la generación de imports pasa por esta clase.
    """

    # ==========================================================
    # Import genérico
    # ==========================================================

    @staticmethod
    def build(
        module: str,
        target: str,
    ) -> str:
        """
        Construye una sentencia import.

        Ejemplo:

            from ..services.producto_service import ProductoService
        """

        return f"from {module} import {target}"

    # ==========================================================
    # Framework
    # ==========================================================

    @classmethod
    def framework(
        cls,
        module: str,
        target: str,
    ) -> str:
        """
        Construye un import del framework interno de VIERNES.

        El framework real está ubicado en:

            agents/framework/

        Por tanto:

            ImportResolver.framework(
                "base_model",
                "Base",
            )

        produce:

            from agents.framework.base_model import Base
        """

        return cls.build(
            f"backend.framework.{module}",
            target,
        )
