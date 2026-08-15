"""
REGRESIÓN RUNTIME — MULTI-FK / CASCADE / RESTRICT

Prueba una base SQLite aislada.

Contrato:

Producto
    |
    | producto_id ON DELETE CASCADE
    v
DetalleProducto

Categoria
    |
    | categoria_id ON DELETE RESTRICT
    v
DetalleProducto
"""

import sys
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

BACKEND = (
    ROOT
    / "workspace"
    / "multi_fk_test"
    / "src"
    / "backend"
)

sys.path.insert(0, str(BACKEND))


# ============================================================
# SQLITE AISLADO
# ============================================================

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# ============================================================
# SQLITE FOREIGN KEYS
# ============================================================

@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


# ============================================================
# IMPORTAR BASE Y MODELOS
# ============================================================

from framework.base_model import Base

from modules.categoria.models.categoria import Categoria
from modules.producto.models.producto import Producto
from modules.detalle_producto.models.detalle_producto import (
    DetalleProducto,
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ============================================================
# CREAR TABLAS
# ============================================================

Base.metadata.create_all(engine)


# ============================================================
# HELPERS
# ============================================================

def assert_exists(session, model, record_id, label):

    result = (
        session
        .query(model)
        .filter(model.id == record_id)
        .first()
    )

    if result is None:
        raise AssertionError(
            f"{label}: registro {record_id} no existe."
        )

    print(
        f"  OK: {label} {record_id} existe"
    )


def assert_missing(session, model, record_id, label):

    result = (
        session
        .query(model)
        .filter(model.id == record_id)
        .first()
    )

    if result is not None:
        raise AssertionError(
            f"{label}: registro {record_id} debería "
            "haber desaparecido."
        )

    print(
        f"  OK: {label} {record_id} fue eliminado"
    )


# ============================================================
# PRUEBA 1 — CASCADE
# ============================================================

print()
print("=" * 60)
print("1. RUNTIME — ON DELETE CASCADE")
print("=" * 60)

session = SessionLocal()

categoria = Categoria(
    nombre="RUNTIME_REGRESSION_CASCADE"
)

session.add(categoria)
session.commit()
session.refresh(categoria)

producto = Producto(
    nombre="RUNTIME_REGRESSION_PRODUCTO",
    categoria_id=categoria.id,
)

session.add(producto)
session.commit()
session.refresh(producto)

detalle = DetalleProducto(
    cantidad=10,
    producto_id=producto.id,
    categoria_id=categoria.id,
)

session.add(detalle)
session.commit()
session.refresh(detalle)

categoria_id = categoria.id
producto_id = producto.id
detalle_id = detalle.id

print(f"Categoria ID: {categoria_id}")
print(f"Producto ID: {producto_id}")
print(f"Detalle ID: {detalle_id}")

assert_exists(
    session,
    Categoria,
    categoria_id,
    "Categoria",
)

assert_exists(
    session,
    Producto,
    producto_id,
    "Producto",
)

assert_exists(
    session,
    DetalleProducto,
    detalle_id,
    "DetalleProducto",
)


print()
print("Eliminando Producto...")

session.delete(producto)
session.commit()


assert_missing(
    session,
    Producto,
    producto_id,
    "Producto",
)

assert_missing(
    session,
    DetalleProducto,
    detalle_id,
    "DetalleProducto",
)


# La Categoria NO debe desaparecer.

assert_exists(
    session,
    Categoria,
    categoria_id,
    "Categoria",
)

print()
print("CASCADE RUNTIME: PASS")

session.close()


# ============================================================
# PRUEBA 2 — RESTRICT
# ============================================================

print()
print("=" * 60)
print("2. RUNTIME — ON DELETE RESTRICT")
print("=" * 60)

session = SessionLocal()

categoria = Categoria(
    nombre="RUNTIME_REGRESSION_RESTRICT"
)

session.add(categoria)
session.commit()
session.refresh(categoria)

producto = Producto(
    nombre="RUNTIME_REGRESSION_RESTRICT_PRODUCTO",
    categoria_id=categoria.id,
)

session.add(producto)
session.commit()
session.refresh(producto)

detalle = DetalleProducto(
    cantidad=5,
    producto_id=producto.id,
    categoria_id=categoria.id,
)

session.add(detalle)
session.commit()
session.refresh(detalle)

categoria_id = categoria.id
producto_id = producto.id
detalle_id = detalle.id

print(f"Categoria ID: {categoria_id}")
print(f"Producto ID: {producto_id}")
print(f"Detalle ID: {detalle_id}")

print()
print("Intentando eliminar Categoria...")

restrict_passed = False

try:

    session.delete(categoria)

    session.commit()

except IntegrityError:

    session.rollback()

    restrict_passed = True

    print(
        "  OK: SQLite rechazó DELETE por "
        "ON DELETE RESTRICT"
    )


if not restrict_passed:

    raise AssertionError(
        "RESTRICT FALLÓ: Categoria fue eliminada "
        "aunque DetalleProducto todavía depende de ella."
    )


assert_exists(
    session,
    Categoria,
    categoria_id,
    "Categoria",
)

assert_exists(
    session,
    Producto,
    producto_id,
    "Producto",
)

assert_exists(
    session,
    DetalleProducto,
    detalle_id,
    "DetalleProducto",
)

print()
print("RESTRICT RUNTIME: PASS")

session.close()


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print("RESULTADO FINAL — RUNTIME MULTI-FK")
print("=" * 60)

print("CASCADE: PASS")
print("RESTRICT: PASS")
print("SQLITE FOREIGN KEYS: ON")
print("RUNTIME REFERENCIAL: OK")
print("=" * 60)
