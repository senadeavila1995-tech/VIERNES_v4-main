from pathlib import Path

from agents.crud.crud_generator import CrudGenerator
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField


# ==========================================================
# CATEGORIA
# ==========================================================

categoria = CrudDefinition(
    entity="Categoria",
    table="categorias",
)


categoria.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=255,
        required=True,
        nullable=False,
    )
)

categoria.add_field(
    CrudField(
        name="descripcion",
        type="string",
        length=255,
        required=True,
        nullable=False,
    )
)


# ==========================================================
# PRODUCTO
# ==========================================================

producto = CrudDefinition(
    entity="Producto",
    table="productos",
)


producto.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=100,
        required=True,
        nullable=False,
    )
)

producto.add_field(
    CrudField(
        name="precio",
        type="float",
        required=True,
        nullable=False,
    )
)

producto.add_field(
    CrudField(
        name="stock",
        type="int",
        required=True,
        nullable=False,
    )
)

producto.add_field(
    CrudField(
        name="categoria_id",
        type="int",
        required=True,
        nullable=False,
        foreign_key=True,
        references="Categoria",
        references_field="id",
    )
)


# ==========================================================
# PROYECTO
# ==========================================================

project = ProjectContext(
    project_name="tienda",
    root_path=Path("workspace/tienda"),
)


# ==========================================================
# CONTEXTO
# ==========================================================

context = GenerationContext(
    definition=producto,
    project=project,
    definitions={
        "categoria": categoria,
        "producto": producto,
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
