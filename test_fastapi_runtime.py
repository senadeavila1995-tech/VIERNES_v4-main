import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# ==========================================================
# PATH PROYECTO GENERADO
# ==========================================================

PROJECT_PATH = Path(
    "workspace/relationship_complex_test/src"
)

BACKEND_PATH = PROJECT_PATH / "backend"

sys.path.insert(
    0,
    str(PROJECT_PATH)
)

sys.path.insert(
    0,
    str(BACKEND_PATH)
)


# ==========================================================
# DATABASE SQLITE TEST
# ==========================================================

from framework.base_model import Base


engine = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)


SessionTest = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ==========================================================
# IMPORT MODELOS
# ==========================================================

from modules.cliente.models.cliente import Cliente
from modules.orden_compra.models.orden_compra import OrdenCompra
from modules.linea_pedido.models.linea_pedido import LineaPedido


Base.metadata.create_all(engine)


# ==========================================================
# FASTAPI
# ==========================================================

from framework.database.session import get_db

from modules.cliente.routes.cliente_route import router as cliente_router


app = FastAPI()


def override_get_db():

    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


app.include_router(
    cliente_router
)


# ==========================================================
# TEST
# ==========================================================

client = TestClient(app)


print("=" * 60)
print("FASTAPI RUNTIME")
print("=" * 60)


response = client.post(
    "/cliente/",
    json={
        "nombre": "Cliente Runtime"
    }
)


print()
print("POST /cliente/")
print("STATUS:", response.status_code)
print(response.json())


response = client.get(
    "/cliente/"
)


print()
print("GET /cliente/")
print("STATUS:", response.status_code)
print(response.json())


assert response.status_code == 200

data = response.json()

assert len(data) == 1
assert data[0]["nombre"] == "Cliente Runtime"


print()
print("=" * 60)
print("FASTAPI RUNTIME OK")
print("=" * 60)
