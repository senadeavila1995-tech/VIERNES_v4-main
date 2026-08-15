"""
REGRESIÓN RUNTIME — MULTI-FK MISMO TARGET

Usuario
   ↑
   ├── Pedido.creado_por_id
   └── Pedido.aprobado_por_id

Objetivo:

1. Importar los modelos generados reales.
2. Construir los mappers SQLAlchemy.
3. Crear dos usuarios.
4. Crear un pedido con creador y aprobador diferentes.
5. Verificar ambas relaciones.
6. Verificar que no existe ambigüedad de FK.
"""

import sys
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# ==========================================================
# PATH
# ==========================================================

ROOT = Path.cwd()

SRC = (
    ROOT
    / "workspace"
    / "multi_fk_same_target_test"
    / "src"
)

BACKEND = SRC / "backend"

sys.path.insert(0, str(SRC))
sys.path.insert(0, str(BACKEND))


# ==========================================================
# DATABASE SQLITE AISLADA
# ==========================================================

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ==========================================================
# IMPORTAR MODELOS GENERADOS
# ==========================================================

print("=" * 60)
print("RUNTIME — MULTI-FK MISMO TARGET")
print("=" * 60)

print()
print("IMPORTANDO MODELOS GENERADOS...")


try:
    from modules.usuario.models.usuario import Usuario
    from modules.pedido.models.pedido import Pedido
except Exception as exc:
    print()
    print("ERROR IMPORTANDO MODELOS:")
    print(exc)
    raise


print("  OK: Usuario")
print("  OK: Pedido")


# ==========================================================
# CREAR TABLAS
# ==========================================================

print()
print("=" * 60)
print("CREANDO TABLAS SQLITE")
print("=" * 60)

try:
    from sqlalchemy.orm import configure_mappers

    Usuario.metadata.create_all(engine)

    configure_mappers()

except Exception as exc:
    print()
    print("ERROR CONFIGURANDO MAPPERS:")
    print(type(exc).__name__)
    print(exc)
    raise


print("  OK: tablas creadas")
print("  OK: SQLAlchemy mappers configurados")


# ==========================================================
# SESIÓN
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

session = SessionLocal()


# ==========================================================
# CREAR USUARIOS
# ==========================================================

print()
print("=" * 60)
print("1. CREAR USUARIOS")
print("=" * 60)

creador = Usuario(
    nombre="CREADOR_RUNTIME"
)

aprobador = Usuario(
    nombre="APROBADOR_RUNTIME"
)

session.add_all(
    [
        creador,
        aprobador,
    ]
)

session.commit()

session.refresh(creador)
session.refresh(aprobador)

print("Creador ID:", creador.id)
print("Aprobador ID:", aprobador.id)

assert creador.id != aprobador.id

print("  OK: usuarios diferentes")


# ==========================================================
# CREAR PEDIDO
# ==========================================================

print()
print("=" * 60)
print("2. CREAR PEDIDO")
print("=" * 60)

pedido = Pedido(
    numero="PEDIDO_RUNTIME_001",
    creado_por_id=creador.id,
    aprobado_por_id=aprobador.id,
)

session.add(pedido)

session.commit()

session.refresh(pedido)

print("Pedido ID:", pedido.id)
print("creado_por_id:", pedido.creado_por_id)
print("aprobado_por_id:", pedido.aprobado_por_id)

assert pedido.creado_por_id == creador.id
assert pedido.aprobado_por_id == aprobador.id

print("  OK: ambas FK apuntan correctamente")


# ==========================================================
# VERIFICAR RELACIÓN CREADOR
# ==========================================================

print()
print("=" * 60)
print("3. VERIFICAR RELACIÓN CREADOR")
print("=" * 60)

print(
    "pedido.creado_por.nombre:",
    pedido.creado_por.nombre,
)

assert pedido.creado_por.id == creador.id
assert pedido.creado_por.nombre == "CREADOR_RUNTIME"

assert pedido.creado_por.id != pedido.aprobado_por.id

print("  OK: Pedido.creado_por")
print("  OK: apunta al Usuario correcto")


# ==========================================================
# VERIFICAR RELACIÓN APROBADOR
# ==========================================================

print()
print("=" * 60)
print("4. VERIFICAR RELACIÓN APROBADOR")
print("=" * 60)

print(
    "pedido.aprobado_por.nombre:",
    pedido.aprobado_por.nombre,
)

assert pedido.aprobado_por.id == aprobador.id
assert pedido.aprobado_por.nombre == "APROBADOR_RUNTIME"

print("  OK: Pedido.aprobado_por")
print("  OK: apunta al Usuario correcto")


# ==========================================================
# VERIFICAR INVERSAS
# ==========================================================

print()
print("=" * 60)
print("5. VERIFICAR RELACIONES INVERSAS")
print("=" * 60)

print(
    "pedidos_creado_por:",
    len(creador.pedidos_creado_por),
)

print(
    "pedidos_aprobado_por:",
    len(aprobador.pedidos_aprobado_por),
)

assert len(creador.pedidos_creado_por) == 1
assert len(aprobador.pedidos_aprobado_por) == 1

assert creador.pedidos_creado_por[0].id == pedido.id
assert aprobador.pedidos_aprobado_por[0].id == pedido.id

print("  OK: Usuario.pedidos_creado_por")
print("  OK: Usuario.pedidos_aprobado_por")


# ==========================================================
# VERIFICAR QUE NO SE CRUZARON
# ==========================================================

print()
print("=" * 60)
print("6. VERIFICAR AISLAMIENTO DE RELACIONES")
print("=" * 60)

assert len(creador.pedidos_aprobado_por) == 0
assert len(aprobador.pedidos_creado_por) == 0

print(
    "  OK: creador NO aparece como aprobador"
)

print(
    "  OK: aprobador NO aparece como creador"
)


# ==========================================================
# RESULTADO
# ==========================================================

session.close()

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print("MAPPERS SQLALCHEMY: PASS")
print("MULTI-FK MISMO TARGET: PASS")
print("CREADO_POR: PASS")
print("APROBADO_POR: PASS")
print("RELACIONES INVERSAS: PASS")
print("AISLAMIENTO DE FK: PASS")
print("RUNTIME REFERENCIAL: OK")
print("=" * 60)
