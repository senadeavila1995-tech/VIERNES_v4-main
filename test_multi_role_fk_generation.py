from pathlib import Path

from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.crud_generator import CrudGenerator


# ==========================================================
# USUARIO
# ==========================================================

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
        length=100,
        required=True,
        nullable=False,
    )
)


# ==========================================================
# PEDIDO
# ==========================================================

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
        name="descripcion",
        type="string",
        length=150,
        required=True,
        nullable=False,
    )
)


# FK creado_por

pedido.add_field(
    CrudField(
        name="creado_por_id",
        type="int",
        required=True,
        nullable=False,
        foreign_key=True,
        references="usuario",
        references_field="id",
        on_delete="RESTRICT",
        on_update="CASCADE",
    )
)


# FK aprobado_por

pedido.add_field(
    CrudField(
        name="aprobado_por_id",
        type="int",
        required=True,
        nullable=False,
        foreign_key=True,
        references="usuario",
        references_field="id",
        on_delete="RESTRICT",
        on_update="CASCADE",
    )
)


pedido.add_dependency("usuario")


# ==========================================================
# PROYECTO
# ==========================================================

project = ProjectContext(
    project_name="multi_role_fk_test",
    root_path=Path(
        "workspace/multi_role_fk_test"
    ),
)


generator = CrudGenerator()


definitions = {
    "usuario": usuario,
    "pedido": pedido,
}


def generate_crud(definition):

    context = GenerationContext(
        definition=definition,
        project=project,
        definitions=definitions,
    )

    print()
    print("=" * 60)
    print(
        f"GENERANDO: {definition.entity}"
    )
    print("=" * 60)

    paths = generator.generate(
        context
    )

    for path in paths:
        print(path)

    print()

    if context.errors:
        print("ERRORES:")
        for error in context.errors:
            print(error)
    else:
        print("OK")


generate_crud(usuario)
generate_crud(pedido)
