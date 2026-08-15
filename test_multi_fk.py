from pathlib import Path

from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.crud_generator import CrudGenerator


# ==========================================================
# CATEGORIA
# ==========================================================

categoria = CrudDefinition(
    entity="Categoria",
    table="categoria",
)

categoria.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)

categoria.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=100,
        required=True,
        nullable=False,
    )
)


# ==========================================================
# PRODUCTO
# ==========================================================

producto = CrudDefinition(
    entity="Producto",
    table="producto",
)

producto.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)

producto.add_field(
    CrudField(
        name="nombre",
        type="string",
        length=150,
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
        references="categoria",
        references_field="id",
        on_delete="RESTRICT",
        on_update="CASCADE",
        index=True,
    )
)


# ==========================================================
# DETALLE PRODUCTO
# ==========================================================

detalle = CrudDefinition(
    entity="DetalleProducto",
    table="detalle_producto",
    timestamps=True,
    soft_delete=True,
)

detalle.add_field(
    CrudField(
        name="id",
        type="int",
        primary_key=True,
        auto_increment=True,
        required=True,
        nullable=False,
    )
)

detalle.add_field(
    CrudField(
        name="cantidad",
        type="int",
        required=True,
        nullable=False,
    )
)

# ----------------------------------------------------------
# FK -> PRODUCTO
# ----------------------------------------------------------

detalle.add_field(
    CrudField(
        name="producto_id",
        type="int",
        required=True,
        nullable=False,
        foreign_key=True,
        references="producto",
        references_field="id",
        on_delete="CASCADE",
        on_update="CASCADE",
        index=True,
    )
)

# ----------------------------------------------------------
# FK -> CATEGORIA
# ----------------------------------------------------------

detalle.add_field(
    CrudField(
        name="categoria_id",
        type="int",
        required=True,
        nullable=False,
        foreign_key=True,
        references="categoria",
        references_field="id",
        on_delete="RESTRICT",
        on_update="CASCADE",
        index=True,
    )
)


# ==========================================================
# DEPENDENCIAS
# ==========================================================

detalle.add_dependency("producto")
detalle.add_dependency("categoria")


# ==========================================================
# PROYECTO
# ==========================================================

project = ProjectContext(
    project_name="multi_fk_test",
    root_path=Path("workspace/multi_fk_test"),
)


# ==========================================================
# GENERADOR
# ==========================================================

generator = CrudGenerator()


# ==========================================================
# FUNCIÓN DE GENERACIÓN
# ==========================================================

def generate_crud(definition: CrudDefinition):

    definitions = {
        "categoria": categoria,
        "producto": producto,
        "detalle_producto": detalle,
    }
    context = GenerationContext(
        definition=definition,
        project=project,
        definitions=definitions,
    )

    print()
    print("=" * 60)
    print(f"GENERANDO: {definition.entity}")
    print("=" * 60)

    paths = generator.generate(context)

    print()
    print("ARCHIVOS GENERADOS:")

    for path in paths:
        print(path)

    print()
    print("ERRORES:")

    if context.errors:
        for error in context.errors:
            print(f"  ERROR: {error}")
    else:
        print("  []")

    return context


# ==========================================================
# GENERAR
# ==========================================================

categoria_context = generate_crud(categoria)

producto_context = generate_crud(producto)

detalle_context = generate_crud(detalle)


# ==========================================================
# VALIDACIÓN FOREIGN KEYS
# ==========================================================

print()
print("=" * 60)
print("VALIDACIÓN ESTRICTA FOREIGN KEYS")
print("=" * 60)


expected_foreign_keys = {
    "producto_id": {
        "references": "producto",
        "references_field": "id",
        "on_delete": "CASCADE",
        "on_update": "CASCADE",
        "index": True,
    },
    "categoria_id": {
        "references": "categoria",
        "references_field": "id",
        "on_delete": "RESTRICT",
        "on_update": "CASCADE",
        "index": True,
    },
}


actual_foreign_keys = {
    field.name: {
        "references": field.references,
        "references_field": field.references_field,
        "on_delete": field.on_delete,
        "on_update": field.on_update,
        "index": field.index,
    }
    for field in detalle.foreign_keys
}


print()
print("FOREIGN KEYS ENCONTRADAS:")

for field in detalle.foreign_keys:

    print(
        f"{field.name} -> "
        f"{field.references}.{field.references_field}"
    )

    print(
        f"  ON DELETE: {field.on_delete}"
    )

    print(
        f"  ON UPDATE: {field.on_update}"
    )

    print(
        f"  INDEX: {field.index}"
    )


print()
print("VALIDANDO CANTIDAD DE FOREIGN KEYS...")

if len(detalle.foreign_keys) != 2:

    raise AssertionError(
        "DetalleProducto debe tener exactamente 2 Foreign Keys. "
        f"Encontradas: {len(detalle.foreign_keys)}"
    )

print("  OK: existen exactamente 2 Foreign Keys.")


print()
print("VALIDANDO DEFINICIONES DE FOREIGN KEYS...")

for field_name, expected in expected_foreign_keys.items():

    if field_name not in actual_foreign_keys:

        raise AssertionError(
            f"Falta la Foreign Key esperada: {field_name}"
        )

    actual = actual_foreign_keys[field_name]

    for attribute, expected_value in expected.items():

        actual_value = actual[attribute]

        if actual_value != expected_value:

            raise AssertionError(
                f"Foreign Key '{field_name}' inválida: "
                f"{attribute}={actual_value!r}, "
                f"esperado={expected_value!r}"
            )

    print(
        f"  OK: {field_name} -> "
        f"{expected['references']}.{expected['references_field']}"
    )


print()
print()
print("VALIDANDO CONFIGURACIÓN ORM DE DELETE...")

producto_model = (
    project.root_path
    / "src"
    / "backend"
    / "modules"
    / "producto"
    / "models"
    / "producto.py"
)

categoria_model = (
    project.root_path
    / "src"
    / "backend"
    / "modules"
    / "categoria"
    / "models"
    / "categoria.py"
)

detalle_model = (
    project.root_path
    / "src"
    / "backend"
    / "modules"
    / "detalle_producto"
    / "models"
    / "detalle_producto.py"
)

producto_text = producto_model.read_text()
categoria_text = categoria_model.read_text()
detalle_text = detalle_model.read_text()

# ----------------------------------------------------------
# Producto -> DetalleProducto
# ON DELETE CASCADE
# ----------------------------------------------------------

if "passive_deletes=True" not in producto_text:
    raise AssertionError(
        "Producto.detalle_productos debe tener "
        "passive_deletes=True por ON DELETE CASCADE."
    )

print(
    "  OK: Producto.detalle_productos -> "
    "passive_deletes=True"
)

# ----------------------------------------------------------
# Categoria -> DetalleProducto
# ON DELETE RESTRICT
# ----------------------------------------------------------

categoria_relation = [
    line
    for line in categoria_text.splitlines()
    if "detalle_productos:" in line
]

if not categoria_relation:
    raise AssertionError(
        "No se encontró Categoria.detalle_productos."
    )

if "passive_deletes=True" in categoria_relation[0]:
    raise AssertionError(
        "Categoria.detalle_productos NO debe tener "
        "passive_deletes=True porque usa ON DELETE RESTRICT."
    )

print(
    "  OK: Categoria.detalle_productos -> "
    "sin passive_deletes"
)

# ----------------------------------------------------------
# Foreign Key producto_id
# ----------------------------------------------------------

if 'ForeignKey("producto.id", ondelete="CASCADE"' not in detalle_text:
    raise AssertionError(
        "producto_id debe tener ON DELETE CASCADE."
    )

print(
    "  OK: producto_id -> "
    "ON DELETE CASCADE"
)

# ----------------------------------------------------------
# Foreign Key categoria_id
# ----------------------------------------------------------

if 'ForeignKey("categoria.id", ondelete="RESTRICT"' not in detalle_text:
    raise AssertionError(
        "categoria_id debe tener ON DELETE RESTRICT."
    )

print(
    "  OK: categoria_id -> "
    "ON DELETE RESTRICT"
)

print()
print("VALIDACIÓN ORM DELETE: OK")

print("VALIDANDO DEPENDENCIAS...")

expected_dependencies = {
    "producto",
    "categoria",
}

actual_dependencies = set(detalle.dependencies)

if actual_dependencies != expected_dependencies:

    raise AssertionError(
        "Dependencias inválidas en DetalleProducto: "
        f"{actual_dependencies!r}. "
        f"Esperadas: {expected_dependencies!r}"
    )

print("  OK: producto")
print("  OK: categoria")


print()
print("VALIDACIÓN MULTI-FK COMPLETA: OK")


# ==========================================================
# RESULTADO
# ==========================================================

all_contexts = [
    categoria_context,
    producto_context,
    detalle_context,
]

errors = [
    error
    for context in all_contexts
    for error in context.errors
]

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

if errors:
    print("GENERACIÓN CON ERRORES")

    for error in errors:
        print(f"  ERROR: {error}")
else:
    print("GENERACIÓN MULTI-FK OK")
