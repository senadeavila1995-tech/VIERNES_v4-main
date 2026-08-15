"""
REGRESSION — MULTI FK SAME TARGET UPDATE API RUNTIME

Valida:

Pedido
 |
 ├── creado_por_id
 └── aprobado_por_id

PUT solamente modifica aprobado_por_id
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
print("MULTI FK SAME TARGET — UPDATE API RUNTIME")
print("=" * 80)


print("\n1. CREAR USUARIOS")


creador = client.post(
    "/usuario/",
    json={
        "nombre": "CREADOR"
    }
).json()


aprobador_original = client.post(
    "/usuario/",
    json={
        "nombre": "APROBADOR_ORIGINAL"
    }
).json()


nuevo_aprobador = client.post(
    "/usuario/",
    json={
        "nombre": "APROBADOR_NUEVO"
    }
).json()


print(creador)
print(aprobador_original)
print(nuevo_aprobador)



print("\n2. CREAR PEDIDO")


pedido = client.post(
    "/pedido/",
    json={
        "numero": "PED-UPDATE",
        "creado_por_id": creador["id"],
        "aprobado_por_id": aprobador_original["id"],
    }
)


print(
    pedido.status_code,
    pedido.json()
)


assert pedido.status_code == 200


pedido_id = pedido.json()["id"]



print("\n3. UPDATE APROBADOR")


response = client.put(
    f"/pedido/{pedido_id}",
    json={
        "aprobado_por_id": nuevo_aprobador["id"]
    }
)


print(
    response.status_code,
    response.json()
)


assert response.status_code == 200


updated = response.json()


assert updated["creado_por_id"] == creador["id"]

assert updated["aprobado_por_id"] == nuevo_aprobador["id"]


print(
    "✓ UPDATE FK CORRECTO"
)



print("\n4. VALIDAR AISLAMIENTO")


assert updated["creado_por"]["id"] == creador["id"]

assert updated["aprobado_por"]["id"] == nuevo_aprobador["id"]


assert (
    updated["creado_por"]["id"]
    !=
    updated["aprobado_por"]["id"]
)


print(
    "✓ RELACIONES NO CRUZADAS"
)



print("\n5. UPDATE FK INVALIDA")


response = client.put(
    f"/pedido/{pedido_id}",
    json={
        "aprobado_por_id": 999999
    }
)


print(
    response.status_code,
    response.json()
)


assert response.status_code == 409


print(
    "✓ UPDATE FK INVALIDA RECHAZADA"
)



print("\n" + "=" * 80)
print(
    "MULTI FK SAME TARGET UPDATE API RUNTIME: PASS"
)
print("=" * 80)

