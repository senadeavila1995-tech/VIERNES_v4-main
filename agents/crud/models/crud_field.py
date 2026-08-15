from dataclasses import dataclass


@dataclass(slots=True)
class CrudField:
    """
    Representa un campo de una entidad.

    Esta definición es independiente del motor de base de datos.
    Posteriormente TypeResolver será el encargado de convertir
    estos tipos genéricos al tipo específico del motor
    (MySQL, PostgreSQL, SQLite, SQL Server, etc.).
    """

    # ==========================================================
    # Información básica
    # ==========================================================

    name: str

    type: str

    description: str = ""

    # ==========================================================
    # Restricciones
    # ==========================================================

    required: bool = True

    nullable: bool = False

    unique: bool = False

    default: str | None = None

    # ==========================================================
    # Claves
    # ==========================================================

    primary_key: bool = False

    auto_increment: bool = False

    # ==========================================================
    # Longitud
    # ==========================================================

    length: int | None = None

    # ==========================================================
    # Tipos numéricos
    # ==========================================================

    precision: int | None = None

    scale: int | None = None

    # ==========================================================
    # Enumeraciones
    # ==========================================================

    enum: list[str] | None = None

    # ==========================================================
    # Relaciones
    # ==========================================================

    foreign_key: bool = False

    references: str | None = None

    references_field: str = "id"

    # ==========================================================
    # Integridad referencial
    # ==========================================================

    on_delete: str | None = None

    on_update: str | None = None

    # ==========================================================
    # Índices
    # ==========================================================

    index: bool = False

    # ==========================================================
    # Restricciones CHECK
    # ==========================================================

    check: str | None = None
