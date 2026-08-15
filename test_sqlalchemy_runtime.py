from pathlib import Path
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ==========================================================
# PATH PROYECTO GENERADO
# ==========================================================

PROJECT = Path(
    "workspace/relationship_complex_test/src/backend"
)

FRAMEWORK = PROJECT.parent / "framework"

sys.path.insert(
    0,
    str(PROJECT)
)

sys.path.insert(
    0,
    str(FRAMEWORK.parent)
)


# ==========================================================
# IMPORT FRAMEWORK BASE
# ==========================================================

from framework.base_model import Base


# ==========================================================
# IMPORT MODELOS GENERADOS
# ==========================================================

from modules.cliente.models.cliente import Cliente
from modules.orden_compra.models.orden_compra import OrdenCompra
from modules.linea_pedido.models.linea_pedido import LineaPedido


# ==========================================================
# DATABASE SQLITE TEST
# ==========================================================

engine = create_engine(
    "sqlite:///:memory:",
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine
)


# ==========================================================
# CREAR TABLAS
# ==========================================================

print("=" * 60)
print("CREANDO TABLAS SQLALCHEMY")
print("=" * 60)


Base.metadata.create_all(
    engine
)


print("TABLAS:")
print(
    Base.metadata.tables.keys()
)


# ==========================================================
# INSERT DATA
# ==========================================================

session = SessionLocal()


cliente = Cliente(
    nombre="Cliente Test"
)


orden = OrdenCompra(
    cliente=cliente
)


linea = LineaPedido(
    orden_compra=orden
)


session.add(
    cliente
)

session.commit()


# ==========================================================
# VALIDAR RELACIONES
# ==========================================================

print()
print("=" * 60)
print("VALIDANDO RELACIONES")
print("=" * 60)


cliente_db = (
    session.query(Cliente)
    .first()
)


print(
    "Cliente:",
    cliente_db.nombre
)


print(
    "Ordenes:",
    len(cliente_db.orden_compras)
)


orden_db = cliente_db.orden_compras[0]


print(
    "Lineas:",
    len(orden_db.linea_pedidos)
)


print()
print("=" * 60)
print("SQLALCHEMY RUNTIME OK")
print("=" * 60)


session.close()
