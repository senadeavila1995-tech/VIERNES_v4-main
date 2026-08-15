from pathlib import Path

from agents.crud.config.crud_structure import CRUD_STRUCTURE
from agents.crud.resolvers.naming_resolver import NamingResolver


class PathResolver:
    """
    Responsable de construir las rutas físicas
    donde se escribirán los archivos generados.
    """

    @staticmethod
    def build(
        output_dir: str,
        layer: str,
        entity: str,
        folder: str,
        filename: str,
    ) -> Path:
        """
        Construye la ruta física de un archivo generado.

        Ejemplo:

            backend/modules/producto/controllers/producto_controller.py

            frontend/modules/producto/pages/ProductoPage.tsx
        """

        # ======================================================
        # ARCHIVOS RAÍZ
        # ======================================================
        #
        # Cuando entity está vacío, el archivo pertenece
        # directamente a la capa.
        #
        # Ejemplo:
        #
        # frontend/App.tsx
        #
        # ======================================================

        if not entity:

            return (
                Path(output_dir)
                / layer
                / folder
                / filename
            )

        # ======================================================
        # ARCHIVOS DE MÓDULO
        # ======================================================

        return (
            Path(output_dir)
            / layer
            / CRUD_STRUCTURE.modules_folder
            / NamingResolver.snake(entity)
            / folder
            / filename
        )
