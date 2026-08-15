from abc import ABC


class BaseRepository(ABC):
    """
    Repositorio base.

    Delega las operaciones de persistencia
    en la capa Database.
    """

    def __init__(self, database):

        self.database = database

    # ==========================================================
    # Crear
    # ==========================================================

    def create(self, model):

        data = self._to_dict(model)

        return self.database.create(data)

    # ==========================================================
    # Buscar
    # ==========================================================

    def get(self, id):

        return self.database.get(id)

    # ==========================================================
    # Listar
    # ==========================================================

    def list(self):

        return self.database.list()

    # ==========================================================
    # Actualizar
    # ==========================================================

    def update(
        self,
        id,
        model,
    ):

        data = self._to_dict(model)

        return self.database.update(
            id,
            data,
        )

    # ==========================================================
    # Eliminar
    # ==========================================================

    def delete(self, id):

        return self.database.delete(id)

    # ==========================================================
    # Conversión
    # ==========================================================

    @staticmethod
    def _to_dict(model):

        if isinstance(model, dict):
            return model

        if hasattr(model, "model_dump"):
            return model.model_dump(
                exclude_unset=True
            )

        if hasattr(model, "to_dict"):
            return model.to_dict()

        if hasattr(model, "__dict__"):
            return {
                key: value
                for key, value in vars(model).items()
                if not key.startswith("_")
            }

        raise TypeError(
            f"No se puede convertir {type(model).__name__} "
            "a dict."
        )
