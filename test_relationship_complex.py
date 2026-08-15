from pathlib import Path

from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField
from agents.crud.models.crud_relationship import CrudRelationship
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.crud_generator import CrudGenerator
from agents.crud.resolvers.naming_resolver import NamingResolver


# ==============================
# CLIENTE
# ==============================

cliente = CrudDefinition(
    entity="Cliente",
    table="cliente",
)

cliente.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)

cliente.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=120,
        required=True,
        nullable=False,
    )
)


# ==============================
# ORDEN_COMPRA
# ==============================

orden = CrudDefinition(
    entity="OrdenCompra",
    table="orden_compra",
)

orden.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)


orden.add_field(
    CrudField(
        name="cliente_id",
        type="int",
        foreign_key=True,
        references="Cliente",
        required=True,
        nullable=False,
    )
)


# ==============================
# LINEA_PEDIDO
# ==============================

linea = CrudDefinition(
    entity="LineaPedido",
    table="linea_pedido",
)

linea.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)

linea.add_field(
    CrudField(
        name="orden_compra_id",
        type="int",
        foreign_key=True,
        references="OrdenCompra",
        required=True,
        nullable=False,
    )
)


definitions = {
    "Cliente": cliente,
    "OrdenCompra": orden,
    "LineaPedido": linea,
}



project = ProjectContext(
    project_name="relationship_complex_test",
    root_path=Path(
        "workspace/relationship_complex_test"
    ),
    source_dir="src",
)


def generate(definition):

    context = GenerationContext(
        project=project,
        definition=definition,
        definitions=definitions,
    )

    generator = CrudGenerator()

    generator.generate(
        context
    )


for definition in definitions.values():

    print("=" * 60)
    print("GENERANDO:", definition.entity)
    print("=" * 60)

    generate(definition)


print("\nTEST RELACIONES COMPLEJAS OK")
