"""
REGRESIÓN — MULTI-FK HACIA LA MISMA ENTIDAD

Usuario
   ↑
   ├── Pedido.creado_por_id
   └── Pedido.aprobado_por_id

Contrato:

Pedido.creado_por
    -> Usuario
    foreign_keys=Pedido.creado_por_id
    back_populates=pedidos_creado_por

Pedido.aprobado_por
    -> Usuario
    foreign_keys=Pedido.aprobado_por_id
    back_populates=pedidos_aprobado_por

Usuario.pedidos_creado_por
    -> Pedido
    foreign_keys=Pedido.creado_por_id
    back_populates=creado_por

Usuario.pedidos_aprobado_por
    -> Pedido
    foreign_keys=Pedido.aprobado_por_id
    back_populates=aprobado_por
"""

from pathlib import Path

from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.crud_field import CrudField
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.crud_generator import CrudGenerator


print("=" * 60)
print("REGRESIÓN — MULTI-FK MISMO TARGET")
print("=" * 60)


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
        name="numero",
        type="string",
        length=50,
        required=True,
        nullable=False,
    )
)


# ----------------------------------------------------------
# FK CREADOR
# ----------------------------------------------------------

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
        index=True,
    )
)


# ----------------------------------------------------------
# FK APROBADOR
# ----------------------------------------------------------

pedido.add_field(
    CrudField(
        name="aprobado_por_id",
        type="int",
        required=False,
        nullable=True,
        foreign_key=True,
        references="usuario",
        references_field="id",
        on_delete="RESTRICT",
        on_update="CASCADE",
        index=True,
    )
)


# ==========================================================
# PROYECTO
# ==========================================================

project = ProjectContext(
    project_name="multi_fk_nullable_test",
    root_path=Path("workspace/multi_fk_nullable_test"),
)

generator = CrudGenerator()


definitions = {
    "usuario": usuario,
    "pedido": pedido,
}


# ==========================================================
# GENERAR USUARIO
# ==========================================================

print()
print("=" * 60)
print("GENERANDO: Usuario")
print("=" * 60)

usuario_context = GenerationContext(
    definition=usuario,
    project=project,
    definitions=definitions,
)

usuario_paths = generator.generate(usuario_context)

print(f"Archivos generados: {len(usuario_paths)}")
print("Errores:", usuario_context.errors)


# ==========================================================
# GENERAR PEDIDO
# ==========================================================

print()
print("=" * 60)
print("GENERANDO: Pedido")
print("=" * 60)

pedido_context = GenerationContext(
    definition=pedido,
    project=project,
    definitions=definitions,
)

pedido_paths = generator.generate(pedido_context)

print(f"Archivos generados: {len(pedido_paths)}")
print("Errores:", pedido_context.errors)


# ==========================================================
# VALIDAR RELACIONES RESUELTAS
# ==========================================================

print()
print("=" * 60)
print("VALIDANDO RELACIONES RESUELTAS")
print("=" * 60)

print()
print("PEDIDO:")

for relation in pedido.relationships:
    print(
        f"  {relation.name} -> {relation.target} | "
        f"type={relation.relation_type} | "
        f"back_populates={relation.back_populates} | "
        f"fk={relation.foreign_key_field}"
    )

print()
print("USUARIO:")

for relation in usuario.relationships:
    print(
        f"  {relation.name} -> {relation.target} | "
        f"type={relation.relation_type} | "
        f"back_populates={relation.back_populates} | "
        f"fk={relation.foreign_key_field}"
    )


# ==========================================================
# EXPECTATIVAS PEDIDO
# ==========================================================

pedido_relations = {
    relation.name: relation
    for relation in pedido.relationships
}

assert "creado_por" in pedido_relations
assert "aprobado_por" in pedido_relations

assert pedido_relations["creado_por"].target == "Usuario"
assert pedido_relations["aprobado_por"].target == "Usuario"

assert pedido_relations["creado_por"].foreign_key_field == "creado_por_id"
assert pedido_relations["aprobado_por"].foreign_key_field == "aprobado_por_id"

assert pedido_relations["creado_por"].back_populates == "pedidos_creado_por"
assert pedido_relations["aprobado_por"].back_populates == "pedidos_aprobado_por"

print()
print("  OK: Pedido.creado_por")
print("  OK: Pedido.aprobado_por")
print("  OK: FK independientes")
print("  OK: back_populates independientes")


# ==========================================================
# EXPECTATIVAS USUARIO
# ==========================================================

usuario_relations = {
    relation.name: relation
    for relation in usuario.relationships
}

assert "pedidos_creado_por" in usuario_relations
assert "pedidos_aprobado_por" in usuario_relations

assert (
    usuario_relations["pedidos_creado_por"].foreign_key_field
    == "creado_por_id"
)

assert (
    usuario_relations["pedidos_aprobado_por"].foreign_key_field
    == "aprobado_por_id"
)

assert (
    usuario_relations["pedidos_creado_por"].back_populates
    == "creado_por"
)

assert (
    usuario_relations["pedidos_aprobado_por"].back_populates
    == "aprobado_por"
)

print()
print("  OK: Usuario.pedidos_creado_por")
print("  OK: Usuario.pedidos_aprobado_por")
print("  OK: FK inversas independientes")
print("  OK: back_populates inversos independientes")


# ==========================================================
# VALIDAR ARCHIVO GENERADO
# ==========================================================

pedido_model = (
    project.root_path
    / "src"
    / "backend"
    / "modules"
    / "pedido"
    / "models"
    / "pedido.py"
)

usuario_model = (
    project.root_path
    / "src"
    / "backend"
    / "modules"
    / "usuario"
    / "models"
    / "usuario.py"
)

assert pedido_model.exists(), (
    f"No existe modelo generado: {pedido_model}"
)

assert usuario_model.exists(), (
    f"No existe modelo generado: {usuario_model}"
)

pedido_text = pedido_model.read_text()
usuario_text = usuario_model.read_text()


# ==========================================================
# VALIDAR GENERACIÓN PEDIDO
# ==========================================================

print()
print("=" * 60)
print("VALIDANDO MODELO GENERADO — PEDIDO")
print("=" * 60)

expected_pedido_creado = (
    'foreign_keys="Pedido.creado_por_id"'
)

expected_pedido_aprobado = (
    'foreign_keys="Pedido.aprobado_por_id"'
)

assert expected_pedido_creado in pedido_text
assert expected_pedido_aprobado in pedido_text

assert (
    'back_populates="pedidos_creado_por"'
    in pedido_text
)

assert (
    'back_populates="pedidos_aprobado_por"'
    in pedido_text
)

print("  OK: Pedido.creado_por -> Pedido.creado_por_id")
print("  OK: Pedido.aprobado_por -> Pedido.aprobado_por_id")
print("  OK: back_populates creador")
print("  OK: back_populates aprobador")


# ==========================================================
# VALIDAR GENERACIÓN USUARIO
# ==========================================================

print()
print("=" * 60)
print("VALIDANDO MODELO GENERADO — USUARIO")
print("=" * 60)

assert (
    'foreign_keys="Pedido.creado_por_id"'
    in usuario_text
)

assert (
    'foreign_keys="Pedido.aprobado_por_id"'
    in usuario_text
)

assert (
    'back_populates="creado_por"'
    in usuario_text
)

assert (
    'back_populates="aprobado_por"'
    in usuario_text
)

print("  OK: Usuario.pedidos_creado_por -> Pedido.creado_por_id")
print("  OK: Usuario.pedidos_aprobado_por -> Pedido.aprobado_por_id")
print("  OK: back_populates creador")
print("  OK: back_populates aprobador")


# ==========================================================
# RESULTADO
# ==========================================================


# ==========================================================
# VALIDAR NULLABLE EN DTO CREATE / RESPONSE / MODEL
# ==========================================================

print()
print("=" * 60)
print("VALIDANDO NULLABLE — aprobado_por_id")
print("=" * 60)

pedido_create_path = (
    Path("workspace/multi_fk_nullable_test")
    / "src/backend/modules/pedido/dto/pedido_create.py"
)

pedido_response_path = (
    Path("workspace/multi_fk_nullable_test")
    / "src/backend/modules/pedido/dto/pedido_response.py"
)

pedido_model_path = (
    Path("workspace/multi_fk_nullable_test")
    / "src/backend/modules/pedido/models/pedido.py"
)


pedido_create_text = pedido_create_path.read_text()
pedido_response_text = pedido_response_path.read_text()
pedido_model_text = pedido_model_path.read_text()


assert "aprobado_por_id: int | None = None" in pedido_create_text

assert "aprobado_por_id: int | None" in pedido_response_text

assert "nullable=True" in pedido_model_text


print("  OK: Create DTO nullable")
print("  OK: Response DTO nullable")
print("  OK: SQLAlchemy nullable")


errors = (
    usuario_context.errors
    + pedido_context.errors
)

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

if errors:
    print("GENERACIÓN CON ERRORES")
    for error in errors:
        print("  ERROR:", error)
    raise SystemExit(1)

print("MULTI-FK MISMO TARGET: PASS")
print("RELATIONSHIPS: PASS")
print("FOREIGN_KEYS: PASS")
print("BACK_POPULATES: PASS")
print("=" * 60)
