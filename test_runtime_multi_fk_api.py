from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient


from backend.main import app

from backend.framework.base_model import Base
from backend.framework.database.session import get_db


# IMPORTANTE
from backend.modules.usuario.models.usuario import Usuario
from backend.modules.pedido.models.pedido import Pedido


print("=" * 60)
print("FASTAPI RUNTIME SQLITE - MULTI FK SAME TARGET")
print("=" * 60)


# ==========================================================
# SQLITE COMPARTIDO EN MEMORIA
# ==========================================================

engine = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


print()
print("CREANDO TABLAS SQLITE")

Base.metadata.create_all(
    bind=engine
)


print("OK")
print(Base.metadata.tables.keys())


# ==========================================================
# OVERRIDE FASTAPI DATABASE
# ==========================================================

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db



# ==========================================================
# CLIENTE
# ==========================================================

client = TestClient(app)



print()
print("=" * 60)
print("CREANDO USUARIOS")
print("=" * 60)


r1 = client.post(
    "/usuario/",
    json={
        "nombre": "Administrador"
    }
)


print(
    r1.status_code,
    r1.json()
)


usuario1 = r1.json()["id"]



r2 = client.post(
    "/usuario/",
    json={
        "nombre": "Supervisor"
    }
)


print(
    r2.status_code,
    r2.json()
)


usuario2 = r2.json()["id"]



print()
print("=" * 60)
print("CREANDO PEDIDO MULTI FK")
print("=" * 60)


pedido = client.post(
    "/pedido/",
    json={
        "numero": "PED-001",
        "creado_por_id": usuario1,
        "aprobado_por_id": usuario2
    }
)


print(
    pedido.status_code,
    pedido.json()
)



print()
print("=" * 60)
print("VALIDANDO RELACIONES")
print("=" * 60)


data = pedido.json()


print(
    "creado_por_id:",
    data["creado_por_id"]
)


print(
    "aprobado_por_id:",
    data["aprobado_por_id"]
)




assert data["creado_por_id"] == usuario1
assert data["aprobado_por_id"] == usuario2


print()
print("=" * 60)
print("CONSULTANDO PEDIDO GET")
print("=" * 60)


get_pedido = client.get(
    f"/pedido/{data['id']}"
)


print(
    get_pedido.status_code,
    get_pedido.json()
)


get_data = get_pedido.json()


assert get_data["creado_por_id"] == usuario1
assert get_data["aprobado_por_id"] == usuario2


assert get_data["creado_por"]["id"] == usuario1
assert get_data["aprobado_por"]["id"] == usuario2


assert get_data["creado_por"]["nombre"] == "Administrador"
assert get_data["aprobado_por"]["nombre"] == "Supervisor"


print()
print("=" * 60)
print("ACTUALIZANDO PEDIDO MULTI FK")
print("=" * 60)


update_pedido = client.put(
    f"/pedido/{data['id']}",
    json={
        "numero": "PED-002",
        "creado_por_id": usuario2,
        "aprobado_por_id": usuario1
    }
)


print(
    update_pedido.status_code,
    update_pedido.json()
)


assert update_pedido.status_code == 200


updated = update_pedido.json()


assert updated["numero"] == "PED-002"
assert updated["creado_por_id"] == usuario2
assert updated["aprobado_por_id"] == usuario1


assert updated["creado_por"]["nombre"] == "Supervisor"
assert updated["aprobado_por"]["nombre"] == "Administrador"


print()
print("=" * 60)
print("UPDATE MULTI-FK SAME TARGET: PASS")
print("=" * 60)



print()
print("=" * 60)
print("ELIMINANDO USUARIO CON PEDIDO EXISTENTE")
print("=" * 60)


delete_usuario = client.delete(
    f"/usuario/{usuario2}"
)


print(
    delete_usuario.status_code,
    delete_usuario.json()
)


assert delete_usuario.status_code in [
    200,
    409
]


print()
print("=" * 60)
print("DELETE USUARIO CON FK VALIDADO")
print("=" * 60)


print()
print("=" * 60)
print("ELIMINANDO PEDIDO MULTI FK")
print("=" * 60)


delete_pedido = client.delete(
    f"/pedido/{data['id']}"
)


print(
    delete_pedido.status_code,
    delete_pedido.json()
)


assert delete_pedido.status_code == 200


print()
print("=" * 60)
print("VALIDANDO QUE PEDIDO NO EXISTE")
print("=" * 60)


check_delete = client.get(
    f"/pedido/{data['id']}"
)


print(
    check_delete.status_code,
    check_delete.json()
)


assert check_delete.status_code == 404


print()
print("=" * 60)
print("DELETE MULTI-FK SAME TARGET: PASS")
print("=" * 60)


print()
print("=" * 60)
print("GET MULTI-FK SAME TARGET: PASS")
print("=" * 60)




print()
print("=" * 60)
print("TEST FK NULLABLE")
print("=" * 60)


pedido_nullable = client.post(
    "/pedido/",
    json={
        "numero": "PED-NULL",
        "creado_por_id": usuario1,
        "aprobado_por_id": None
    }
)


print(
    pedido_nullable.status_code,
    pedido_nullable.json()
)


assert pedido_nullable.status_code == 200


nullable_data = pedido_nullable.json()


assert nullable_data["aprobado_por_id"] is None


print()
print("=" * 60)
print("GET PEDIDO SIN APROBADOR")
print("=" * 60)


get_nullable = client.get(
    f"/pedido/{nullable_data['id']}"
)


print(
    get_nullable.status_code,
    get_nullable.json()
)


assert get_nullable.json()["aprobado_por"] is None


print()
print("=" * 60)
print("AGREGANDO APROBADOR")
print("=" * 60)


update_nullable = client.put(
    f"/pedido/{nullable_data['id']}",
    json={
        "numero": "PED-NULL-OK",
        "creado_por_id": usuario1,
        "aprobado_por_id": usuario2
    }
)


print(
    update_nullable.status_code,
    update_nullable.json()
)


assert update_nullable.json()["aprobado_por_id"] == usuario2


print()
print("=" * 60)
print("QUITANDO APROBADOR")
print("=" * 60)


remove_nullable = client.put(
    f"/pedido/{nullable_data['id']}",
    json={
        "numero": "PED-NULL-FINAL",
        "creado_por_id": usuario1,
        "aprobado_por_id": None
    }
)


print(
    remove_nullable.status_code,
    remove_nullable.json()
)


assert remove_nullable.json()["aprobado_por_id"] is None


print()
print("=" * 60)
print("FK NULLABLE: PASS")
print("=" * 60)


print()
print("=" * 60)
print("MULTI-FK SAME TARGET API: PASS")
print("=" * 60)

