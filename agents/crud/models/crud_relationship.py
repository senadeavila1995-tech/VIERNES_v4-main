from dataclasses import dataclass


@dataclass(slots=True)
class CrudRelationship:
    """
    Representa una relación ORM SQLAlchemy.

    Ejemplo:

    Producto -> Categoria

    categoria = relationship(
        "Categoria",
        back_populates="productos"
    )
    """

    name: str

    target: str

    relation_type: str = "many_to_one"

    back_populates: str | None = None

    # Campo FK que origina la relación.
    #
    # Ejemplo:
    #
    # Pedido.creado_por_id
    # Pedido.aprobado_por_id
    #
    # permiten diferenciar múltiples FK
    # hacia la misma entidad.
    #
    foreign_key_field: str | None = None

    # Acción ON DELETE de la FK que origina la relación.
    #
    # Ejemplo:
    #
    # producto_id -> Producto.id
    # on_delete = "CASCADE"
    #
    # Se utiliza por el ModelGenerator para decidir si
    # SQLAlchemy debe delegar el borrado en la FK mediante
    # passive_deletes=True.
    on_delete: str | None = None

    lazy: str | None = None
