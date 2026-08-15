from pathlib import Path

from agents.crud.crud_generator import CrudGenerator
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField


definition = CrudDefinition(
    entity="Producto",
    table="producto",
    fields=[
        CrudField(
            name="nombre",
            type="string",
            required=True,
        ),
        CrudField(
            name="precio",
            type="float",
            required=True,
        ),
        CrudField(
            name="stock",
            type="integer",
            required=True,
        ),
    ],
)


project = ProjectContext(
    project_name="tienda",
    root_path=Path("workspace/tienda"),
)


context = GenerationContext(
    definition=definition,
    project=project,
    definitions={
        "producto": definition
    }
)


generator = CrudGenerator()

files = generator.generate(context)

print("GENERADO:", len(files))
