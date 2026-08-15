class BaseService:
    """
    Servicio base.

    Contiene la lógica de aplicación y delega
    persistencia al Repository.
    """

    def __init__(self, repository):

        self.repository = repository

    # ==========================================================
    # Crear
    # ==========================================================

    def create(self, model):

        return self.repository.create(model)

    # ==========================================================
    # Buscar
    # ==========================================================

    def get(self, id):

        return self.repository.get(id)

    # ==========================================================
    # Listar
    # ==========================================================

    def list(self):

        return self.repository.list()

    # ==========================================================
    # Actualizar
    # ==========================================================

    def update(
        self,
        id,
        model,
    ):

        return self.repository.update(
            id,
            model,
        )

    # ==========================================================
    # Eliminar
    # ==========================================================

    def delete(self, id):

        return self.repository.delete(id)
