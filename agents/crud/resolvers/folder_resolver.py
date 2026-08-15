from pathlib import Path

from agents.crud.config.crud_structure import CRUD_STRUCTURE
from agents.crud.resolvers.naming_resolver import NamingResolver

class FolderResolver:
    """
    Responsable de resolver y crear la estructura física
    del motor CRUD.

    Toda la configuración se obtiene desde CRUD_STRUCTURE.
    """

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def exists(kind: str) -> bool:
        """
        Indica si un tipo CRUD existe.
        """

        return kind in CRUD_STRUCTURE.crud_types

    @classmethod
    def config(
        cls,
        kind: str,
    ) -> dict:
        """
        Devuelve la configuración completa de un tipo CRUD.
        """

        if not cls.exists(kind):
            raise ValueError(f"Tipo CRUD desconocido: {kind}")

        return CRUD_STRUCTURE.crud_types[kind]

    # ==========================================================
    # Resolución lógica
    # ==========================================================

    @classmethod
    def resolve(
        cls,
        kind: str,
    ) -> str:
        """
        Devuelve la carpeta lógica correspondiente
        al tipo solicitado.
        """

        return cls.config(kind)["folder"]

    @classmethod
    def layer(
        cls,
        kind: str,
    ) -> str:
        """
        Devuelve la capa a la que pertenece el tipo.

        Ejemplo:

            controller -> backend
            page       -> frontend
        """

        return cls.config(kind)["layer"]

    # ==========================================================
    # Carpetas por capa
    # ==========================================================

    @classmethod
    def folders(
        cls,
        layer: str,
    ) -> tuple[str, ...]:
        """
        Devuelve todas las carpetas configuradas
        para una capa determinada.
        """

        return tuple(
            sorted(
                {
                    config["folder"]
                    for config in CRUD_STRUCTURE.crud_types.values()
                    if config["layer"] == layer
                }
            )
        )

    # ==========================================================
    # Creación estructura física
    # ==========================================================

    @classmethod
    def create_entity_structure(
        cls,
        output_dir: str,
        entity: str,
    ) -> None:
        """
        Crea automáticamente la estructura del módulo
        separando backend y frontend.

        Backend:
            crea __init__.py

        Frontend:
            no crea __init__.py
        """

        for layer in CRUD_STRUCTURE.layers:

            base = (
                Path(output_dir)
                / layer
                / CRUD_STRUCTURE.modules_folder
                / NamingResolver.snake(entity)
            )

            base.mkdir(
                parents=True,
                exist_ok=True,
            )

            # ----------------------------------------------
            # Solo backend utiliza __init__.py
            # ----------------------------------------------

            if layer == CRUD_STRUCTURE.backend_folder:

                (base / CRUD_STRUCTURE.init_file).touch(
                    exist_ok=True,
                )

            # ----------------------------------------------
            # Carpetas de la capa
            # ----------------------------------------------

            for folder in cls.folders(layer):

                folder_path = base / folder

                folder_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                # Solo backend
                if layer == CRUD_STRUCTURE.backend_folder:

                    (
                        folder_path / CRUD_STRUCTURE.init_file
                    ).touch(
                        exist_ok=True,
                    )