from collections import Counter

from agents.crud.models.crud_relationship import CrudRelationship
from agents.crud.resolvers.naming_resolver import NamingResolver


class RelationshipResolver:
    """
    Construye relaciones ORM entre entidades CRUD.

    Regla de nombres inversos:

    - Una sola FK hacia un target:
        Cliente.orden_compras

    - Múltiples FK hacia el mismo target:
        Usuario.pedidos_creado_por
        Usuario.pedidos_aprobado_por
    """

    @classmethod
    def resolve(cls, definitions):

        print("\n============================================================")
        print("RELATIONSHIP RESOLVER — INICIO")
        print("============================================================")

        for definition in definitions.values():

            print(
                f"[ANTES] {definition.entity}: "
                f"{len(definition.relationships)} relaciones"
            )

            for relation in definition.relationships:
                print(
                    f"    - {relation.name} -> "
                    f"{relation.target} | "
                    f"{relation.relation_type} | "
                    f"back_populates={relation.back_populates} | "
                    f"fk={relation.foreign_key_field}"
                )

            foreign_keys = definition.foreign_keys

            target_counts = Counter(
                field.references
                for field in foreign_keys
            )

            for field in foreign_keys:

                target = field.references

                target_definition = definitions.get(target)

                if not target_definition:
                    continue

                relation_name = field.name

                if relation_name.endswith("_id"):
                    relation_name = relation_name[:-3]

                plural_name = NamingResolver.plural(
                    definition.table
                )

                multiple_to_same_target = (
                    target_counts[target] > 1
                )

                if multiple_to_same_target:

                    inverse_name = (
                        plural_name
                        + "_"
                        + relation_name
                    )

                else:

                    inverse_name = plural_name

                definition.add_relationship(
                    CrudRelationship(
                        name=relation_name,
                        target=target_definition.entity,
                        relation_type="many_to_one",
                        back_populates=inverse_name,
                        foreign_key_field=field.name,
                        on_delete=field.on_delete,
                    )
                )

                target_definition.add_relationship(
                    CrudRelationship(
                        name=inverse_name,
                        target=definition.entity,
                        relation_type="one_to_many",
                        back_populates=relation_name,
                        foreign_key_field=field.name,
                        on_delete=field.on_delete,
                    )
                )

        return definitions
