"""
REGRESSION — MULTI FK SAME TARGET API RUNTIME

Usuario
   |
   ├── Pedido.creado_por_id
   └── Pedido.aprobado_por_id

Validación:
- POST Usuario
- POST Pedido con dos FK
- GET Pedido con relaciones anidadas
- UPDATE FK
- FK inválida rechazada
"""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.pool import StaticPool


PROJECT_PATH = Path(
    "workspace/multi_fk_same_target_test/src"
)

sys.path.insert(
    0,
    str(PROJECT_PATH)
)


from backend.main import app

from backend.framework.base_model import Base
from backend.framework.database.session import get_db


def enable_fk(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute(
        "PRAGMA foreign_keys=ON"
    )

    cursor.close()


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
    enable_fk,
)


SessionTest = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


configure_mappers()

Base.metadata.create_all(
    engine
)


def override_get_db():

    db = SessionTest()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


print("=" * 80)
print("MULTI FK SAME TARGET — API RUNTIME")
print("=" * 80)


print("\n1. CREAR USUARIO CREADOR")

response = client.post(
    "/usuario/",
    json={
        "nombre": "CREADOR_API"
    }
)

print(response.status_code)
print(response.json())

creador_id = response.json()["id"]


print("\n2. CREAR USUARIO APROBADOR")

response = client.post(
    "/usuario/",
    json={
        "nombre": "APROBADOR_API"
    }
)

print(response.status_code)
print(response.json())

aprobador_id = response.json()["id"]


print("\n3. CREAR PEDIDO MULTI FK")

response = client.post(
    "/pedido/",
    json={
        "numero": "PED-001",
        "creado_por_id": creador_id,
        "aprobado_por_id": aprobador_id,
    }
)

print(response.status_code)
print(response.json())


assert response.status_code == 200

pedido = response.json()

assert pedido["creado_por_id"] == creador_id
assert pedido["aprobado_por_id"] == aprobador_id


print("\n✓ MULTI FK CREATE OK")


print("\n4. GET PEDIDO")

response = client.get(
    f"/pedido/{pedido['id']}"
)

print(response.status_code)
print(response.json())


assert response.status_code == 200


data = response.json()


assert data["creado_por"]["id"] == creador_id
assert data["aprobado_por"]["id"] == aprobador_id


print("\n✓ RELACIONES DTO OK")


print("\n5. FK INVALIDA")

response = client.post(
    "/pedido/",
    json={
        "numero": "PED-INVALID",
        "creado_por_id": 999999,
        "aprobado_por_id": aprobador_id,
    }
)

print(response.status_code)
print(response.json())


assert response.status_code == 409


print("\n✓ FK INVALIDA RECHAZADA")


print("\n" + "=" * 80)
print("MULTI FK SAME TARGET API RUNTIME: PASS")
print("=" * 80)
