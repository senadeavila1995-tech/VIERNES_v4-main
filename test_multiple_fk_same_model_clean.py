from pathlib import Path

from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField
from agents.crud.models.crud_relationship import CrudRelationship
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.crud_generator import CrudGenerator
from agents.crud.resolvers.naming_resolver import NamingResolver


# ==============================
# USUARIO
# ==============================

usuario = CrudDefinition(
    entity="Usuario",
    table="usuario",
)


usuario.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)


usuario.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=120,
        required=True,
        nullable=False,
    )
)


# ==============================
# PEDIDO
# ==============================

pedido = CrudDefinition(
    entity="Pedido",
    table="pedido",
)


pedido.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)


pedido.add_field(
    CrudField(
        name="creado_por_id",
        type="int",
        foreign_key=True,
        references="Usuario",
        required=True,
        nullable=False,
    )
)


pedido.add_field(
    CrudField(
        name="aprobado_por_id",
        type="int",
        foreign_key=True,
        references="Usuario",
        required=True,
        nullable=False,
    )
)


definitions = {
    "Usuario": usuario,
    "Pedido": pedido,
}




project = ProjectContext(
    project_name="multiple_fk_same_model_test",
    root_path=Path(
        "workspace/multiple_fk_same_model_test"
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


print()
print("TEST MULTIPLE FK SAME MODEL OK")
