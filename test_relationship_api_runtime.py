import sys
from pathlib import Path

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.pool import StaticPool


# ==========================================================
# PATHS
# ==========================================================

PROJECT_PATH = Path(
    "workspace/relationship_complex_test/src"
)

sys.path.insert(0, str(PROJECT_PATH))


# ==========================================================
# SQLITE — FOREIGN KEYS ON
# ==========================================================

def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


# ==========================================================
# IMPORTS — APP GENERADA REAL
# ==========================================================

from backend.main import app

from backend.framework.base_model import Base
from backend.framework.database.session import get_db

from backend.modules.cliente.models.cliente import Cliente
from backend.modules.orden_compra.models.orden_compra import OrdenCompra
from backend.modules.linea_pedido.models.linea_pedido import LineaPedido


# ==========================================================
# SQLITE AISLADO
# ==========================================================

engine = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

event.listen(
    engine,
    "connect",
    _enable_sqlite_foreign_keys,
)

SessionTest = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ==========================================================
# SQLALCHEMY
# ==========================================================

configure_mappers()

Base.metadata.create_all(engine)


# ==========================================================
# DATABASE OVERRIDE
# ==========================================================

def override_get_db():

    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ==========================================================
# CLIENT
# ==========================================================

client = TestClient(app)


# ==========================================================
# TEST
# ==========================================================

print("=" * 80)
print("RELATIONSHIP API RUNTIME — GENERATED APP REGRESSION")
print("=" * 80)


# ==========================================================
# 1. TABLAS
# ==========================================================

print()
print("1. TABLAS")
print("-" * 80)

tables = sorted(Base.metadata.tables.keys())

print("TABLAS:", tables)

assert "cliente" in tables
assert "orden_compra" in tables
assert "linea_pedido" in tables

print("✓ Tablas registradas")


# ==========================================================
# 2. POST CLIENTE
# ==========================================================

print()
print("2. POST /cliente/")
print("-" * 80)

response = client.post(
    "/cliente/",
    json={
        "nombre": "Cliente Regression",
    },
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

cliente_data = response.json()

assert cliente_data["id"] == 1
assert cliente_data["nombre"] == "Cliente Regression"

cliente_id = cliente_data["id"]

print("✓ Cliente creado:", cliente_id)


# ==========================================================
# 3. POST ORDEN
# ==========================================================

print()
print("3. POST /orden_compra/")
print("-" * 80)

response = client.post(
    "/orden_compra/",
    json={
        "cliente_id": cliente_id,
    },
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

orden_data = response.json()

assert orden_data["id"] == 1
assert orden_data["cliente_id"] == cliente_id

assert "cliente" in orden_data
assert orden_data["cliente"] is not None

assert orden_data["cliente"]["id"] == cliente_id
assert orden_data["cliente"]["nombre"] == "Cliente Regression"

orden_id = orden_data["id"]

print("✓ Orden creada:", orden_id)
print("✓ Orden → Cliente")


# ==========================================================
# 4. POST LINEA
# ==========================================================

print()
print("4. POST /linea_pedido/")
print("-" * 80)

response = client.post(
    "/linea_pedido/",
    json={
        "orden_compra_id": orden_id,
    },
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

linea_data = response.json()

assert linea_data["id"] == 1
assert linea_data["orden_compra_id"] == orden_id

assert "orden_compra" in linea_data
assert linea_data["orden_compra"] is not None

assert linea_data["orden_compra"]["id"] == orden_id
assert linea_data["orden_compra"]["cliente_id"] == cliente_id

print("✓ Línea creada:", linea_data["id"])
print("✓ Línea → Orden")


# ==========================================================
# 5. GET CLIENTE
# ==========================================================

print()
print("5. GET /cliente/")
print("-" * 80)

response = client.get(
    "/cliente/",
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

clientes = response.json()

assert len(clientes) == 1
assert clientes[0]["id"] == cliente_id
assert clientes[0]["nombre"] == "Cliente Regression"

print("✓ GET cliente OK")


# ==========================================================
# 6. GET ORDEN
# ==========================================================

print()
print("6. GET /orden_compra/")
print("-" * 80)

response = client.get(
    "/orden_compra/",
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

ordenes = response.json()

assert len(ordenes) == 1

orden = ordenes[0]

assert orden["id"] == orden_id
assert orden["cliente_id"] == cliente_id

assert orden["cliente"]["id"] == cliente_id
assert orden["cliente"]["nombre"] == "Cliente Regression"

print("✓ GET orden OK")
print("✓ GET orden → Cliente")


# ==========================================================
# 7. GET LINEA
# ==========================================================

print()
print("7. GET /linea_pedido/")
print("-" * 80)

response = client.get(
    "/linea_pedido/",
)

print("STATUS:", response.status_code)
print("JSON  :", response.json())

assert response.status_code == 200

lineas = response.json()

assert len(lineas) == 1

linea = lineas[0]

assert linea["id"] == 1
assert linea["orden_compra_id"] == orden_id

assert linea["orden_compra"]["id"] == orden_id
assert linea["orden_compra"]["cliente_id"] == cliente_id

print("✓ GET línea OK")
print("✓ GET línea → Orden")


# ==========================================================
# FINAL
# ==========================================================

print()
print("=" * 80)
print("✓ GENERATED APP — RELATIONSHIP REGRESSION OK")
print("=" * 80)
