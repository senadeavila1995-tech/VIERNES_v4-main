"""
REGRESIÓN RUNTIME REAL MYSQL

Caso crítico:

Usuario
   |
   +-- Pedido.creado_por_id
   |
   +-- Pedido.aprobado_por_id (nullable)

Valida:

- POST Usuario
- POST Pedido
- FK nullable
- Relaciones múltiples al mismo modelo
- PUT asignando segunda FK
- GET con relaciones anidadas
"""

import os
import sys

from fastapi.testclient import TestClient


PROJECT_PATH = (
    "workspace/multi_fk_nullable_runtime_test/src"
)

sys.path.insert(
    0,
    PROJECT_PATH,
)


# ==========================================================
# MYSQL REAL
# ==========================================================

os.environ["DB_DRIVER"] = "mysql"
os.environ["DB_NAME"] = "viernes_db"


from backend.main import app


client = TestClient(app)


print("=" * 70)
print("MYSQL RUNTIME MULTI FK NULLABLE")
print("=" * 70)


# ==========================================================
# 1. USUARIOS
# ==========================================================

print("\n1. CREAR USUARIO CARLOS")

response = client.post(
    "/usuario/",
    json={
        "nombre": "Carlos Test",
    },
)

print(response.status_code, response.json())

assert response.status_code == 200

carlos = response.json()

carlos_id = carlos["id"]


print("\n2. CREAR USUARIO ANA")

response = client.post(
    "/usuario/",
    json={
        "nombre": "Ana Test",
    },
)

print(response.status_code, response.json())

assert response.status_code == 200

ana = response.json()

ana_id = ana["id"]


# ==========================================================
# 2. PEDIDO SIN APROBADOR
# ==========================================================

print("\n3. CREAR PEDIDO SIN APROBADOR")

response = client.post(
    "/pedido/",
    json={
        "numero": "PED-TEST-001",
        "creado_por_id": carlos_id,
    },
)

print(response.status_code, response.json())

assert response.status_code == 200

pedido = response.json()

pedido_id = pedido["id"]


assert pedido["creado_por_id"] == carlos_id

assert pedido["aprobado_por_id"] is None

assert pedido["creado_por"]["nombre"] == "Carlos Test"

assert pedido["aprobado_por"] is None


print("OK: FK nullable")


# ==========================================================
# 3. ASIGNAR APROBADOR
# ==========================================================

print("\n4. ACTUALIZAR APROBADOR")

response = client.put(
    f"/pedido/{pedido_id}",
    json={
        "aprobado_por_id": ana_id,
    },
)

print(response.status_code, response.json())

assert response.status_code == 200


pedido = response.json()


assert pedido["creado_por"]["id"] == carlos_id

assert pedido["aprobado_por"]["id"] == ana_id

assert pedido["aprobado_por"]["nombre"] == "Ana Test"


print("OK: ambas relaciones funcionando")


# ==========================================================
# 4. GET FINAL
# ==========================================================

print("\n5. GET PEDIDO")


response = client.get(
    f"/pedido/{pedido_id}"
)


print(response.status_code, response.json())


assert response.status_code == 200


pedido = response.json()


assert pedido["creado_por"] is not None

assert pedido["aprobado_por"] is not None


print("\n" + "=" * 70)
print("TEST MYSQL MULTI FK NULLABLE PASSED")
print("=" * 70)
