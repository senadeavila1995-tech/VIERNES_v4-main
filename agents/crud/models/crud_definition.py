from dataclasses import dataclass, field, asdict

from .crud_field import CrudField
from .crud_relationship import CrudRelationship



@dataclass(slots=True)
class CrudDefinition:
    """
    Define completamente una entidad CRUD.

    Esta clase representa el modelo lógico de una tabla
    independientemente del motor de base de datos.
    """

    # ==========================================================
    # Información básica
    # ==========================================================

    entity: str
    table: str

    # ==========================================================
    # Campos
    # ==========================================================

    fields: list[CrudField] = field(default_factory=list)

    # ==========================================================
    # Relaciones ORM
    # ==========================================================

    relationships: list[CrudRelationship] = field(
        default_factory=list
    )

    # ==========================================================
    # Características
    # ==========================================================

    timestamps: bool = True

    soft_delete: bool = False

    auth: bool = False

    description: str = ""

    # ==========================================================
    # Relaciones
    # ==========================================================

    dependencies: list[str] = field(default_factory=list)

    # ==========================================================
    # Métodos
    # ==========================================================

    def add_relationship(
        self,
        relationship: CrudRelationship,
    ) -> None:

        for existing in self.relationships:

            if (
                existing.name == relationship.name
                and existing.target == relationship.target
                and existing.back_populates == relationship.back_populates
                and existing.relation_type == relationship.relation_type
                and existing.foreign_key_field == relationship.foreign_key_field
            ):
                return

        self.relationships.append(
            relationship
        )


    def add_field(
        self,
        field: CrudField,
    ) -> None:

        self.fields.append(field)

    def add_dependency(
        self,
        table: str,
    ) -> None:

        if table not in self.dependencies:
            self.dependencies.append(table)

    # ==========================================================
    # SERIALIZACION
    # ==========================================================

    def to_dict(self):

        return {
            "entity": self.entity,
            "table": self.table,

            "fields": [
                asdict(field)
                for field in self.fields
            ],

            "relationships": [
                asdict(relationship)
                for relationship in self.relationships
            ],

            "timestamps": self.timestamps,
            "soft_delete": self.soft_delete,
            "auth": self.auth,
            "description": self.description,
            "dependencies": self.dependencies,
        }



    # ==========================================================
    # Consultas
    # ==========================================================

    @property
    def primary_keys(self):

        return [field for field in self.fields if field.primary_key]

    @property
    def required_fields(self):

        return [field for field in self.fields if field.required]

    @property
    def nullable_fields(self):

        return [field for field in self.fields if field.nullable]

    @property
    def unique_fields(self):

        return [field for field in self.fields if field.unique]

    @property
    def indexed_fields(self):

        return [field for field in self.fields if field.index]

    @property
    def foreign_keys(self):

        return [field for field in self.fields if field.foreign_key]

    @property
    def has_foreign_keys(self) -> bool:

        return bool(self.foreign_keys)

    @property
    def has_indexes(self) -> bool:

        return bool(self.indexed_fields)

    @property
    def has_soft_delete(self) -> bool:

        return self.soft_delete

    @property
    def has_timestamps(self) -> bool:

        return self.timestamps
