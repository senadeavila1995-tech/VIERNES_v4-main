from pathlib import Path

from agents.crud.crud_generator import CrudGenerator
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField


definition = CrudDefinition(
    entity="Producto",
    table="productos",
)


definition.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=100,
        required=True,
        nullable=False,
    )
)

definition.add_field(
    CrudField(
        name="precio",
        type="float",
        required=True,
        nullable=False,
    )
)

definition.add_field(
    CrudField(
        name="stock",
        type="int",
        required=True,
        nullable=False,
    )
)


project = ProjectContext(
    project_name="tienda",
    root_path=Path("workspace/tienda"),
)


context = GenerationContext(
    definition=definition,
    project=project,
    definitions={
        "producto": definition,
    },
)


generator = CrudGenerator()


paths = generator.generate(context)


print("=" * 60)
print("GENERADO:", len(paths))
print("ERRORES:", context.errors)
print("=" * 60)

for path in paths:
    print(path)
