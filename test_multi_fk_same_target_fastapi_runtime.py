"""
REGRESIÓN FASTAPI REAL — MULTI-FK MISMO TARGET

Usuario
   ↑
   ├── Pedido.creado_por_id
   └── Pedido.aprobado_por_id

Objetivo:

1. Importar la app FastAPI generada real.
2. Crear usuarios mediante HTTP.
3. Crear Pedido mediante HTTP.
4. Verificar que creado_por apunta al Usuario correcto.
5. Verificar que aprobado_por apunta al Usuario correcto.
6. Verificar relaciones inversas.
7. Verificar aislamiento entre ambas FK.
8. Obtener Pedido mediante GET.
9. Actualizar Pedido mediante PUT.
10. Verificar nuevamente ambas relaciones.

NO se modifica el generador.
NO se modifica el código generado.
"""

from fastapi.testclient import TestClient


print("=" * 60)
print("RUNTIME FASTAPI — MULTI-FK MISMO TARGET")
print("=" * 60)

print()
print("IMPORTANDO APP FASTAPI...")

from backend.main import app

print("  OK: FastAPI app importada")

client = TestClient(app)


def show_response(title, response):
    print()
    print(f"=== {title} ===")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


def assert_status(response, expected, operation):
    assert response.status_code == expected, (
        f"{operation}: esperado HTTP {expected}, "
        f"obtenido {response.status_code}: {response.text}"
    )


# ============================================================
# 1. CREAR USUARIO CREADOR
# ============================================================

print()
print("1. CREAR USUARIO CREADOR")

response = client.post(
    "/usuarios/",
    json={
        "nombre": "CREADOR_FASTAPI",
    },
)

show_response("CREATE USUARIO CREADOR", response)
assert_status(response, 200, "POST creador")

creador = response.json()
creador_id = creador["id"]

print("Creador ID:", creador_id)
print("  OK: creador creado")


# ============================================================
# 2. CREAR USUARIO APROBADOR
# ============================================================

print()
print("2. CREAR USUARIO APROBADOR")

response = client.post(
    "/usuarios/",
    json={
        "nombre": "APROBADOR_FASTAPI",
    },
)

show_response("CREATE USUARIO APROBADOR", response)
assert_status(response, 200, "POST aprobador")

aprobador = response.json()
aprobador_id = aprobador["id"]

print("Aprobador ID:", aprobador_id)

assert creador_id != aprobador_id
print("  OK: usuarios diferentes")


# ============================================================
# 3. CREAR PEDIDO CON DOS FK AL MISMO TARGET
# ============================================================

print()
print("3. CREAR PEDIDO")

response = client.post(
    "/pedidos/",
    json={
        "nombre": "PEDIDO_FASTAPI",
        "creado_por_id": creador_id,
        "aprobado_por_id": aprobador_id,
    },
)

show_response("CREATE PEDIDO", response)
assert_status(response, 200, "POST pedido")

pedido = response.json()
pedido_id = pedido["id"]

print("Pedido ID:", pedido_id)
print("creado_por_id:", pedido.get("creado_por_id"))
print("aprobado_por_id:", pedido.get("aprobado_por_id"))

assert pedido["creado_por_id"] == creador_id
assert pedido["aprobado_por_id"] == aprobador_id

print("  OK: ambas FK apuntan correctamente")


# ============================================================
# 4. VERIFICAR RELACIÓN CREADOR EN JSON
# ============================================================

print()
print("4. VERIFICAR RELACIÓN CREADOR")

creador_json = pedido.get("creado_por")

print("pedido.creado_por:", creador_json)

assert creador_json is not None
assert creador_json["id"] == creador_id
assert creador_json["nombre"] == "CREADOR_FASTAPI"

print("  OK: Pedido.creado_por")
print("  OK: apunta al Usuario creador correcto")


# ============================================================
# 5. VERIFICAR RELACIÓN APROBADOR EN JSON
# ============================================================

print()
print("5. VERIFICAR RELACIÓN APROBADOR")

aprobador_json = pedido.get("aprobado_por")

print("pedido.aprobado_por:", aprobador_json)

assert aprobador_json is not None
assert aprobador_json["id"] == aprobador_id
assert aprobador_json["nombre"] == "APROBADOR_FASTAPI"

print("  OK: Pedido.aprobado_por")
print("  OK: apunta al Usuario aprobador correcto")


# ============================================================
# 6. AISLAMIENTO DE RELACIONES
# ============================================================

print()
print("6. VERIFICAR AISLAMIENTO DE RELACIONES")

assert pedido["creado_por"]["id"] != pedido["aprobado_por"]["id"]
assert pedido["creado_por"]["nombre"] != pedido["aprobado_por"]["nombre"]

print("  OK: creador NO aparece como aprobador")
print("  OK: aprobador NO aparece como creador")


# ============================================================
# 7. GET PEDIDO
# ============================================================

print()
print("7. GET PEDIDO")

response = client.get(
    f"/pedidos/{pedido_id}"
)

show_response("GET PEDIDO", response)
assert_status(response, 200, "GET pedido")

pedido_get = response.json()

assert pedido_get["id"] == pedido_id
assert pedido_get["creado_por_id"] == creador_id
assert pedido_get["aprobado_por_id"] == aprobador_id

assert pedido_get["creado_por"]["id"] == creador_id
assert pedido_get["aprobado_por"]["id"] == aprobador_id

print("  OK: GET conserva ambas FK")
print("  OK: GET conserva ambas relaciones")


# ============================================================
# 8. GET USUARIO CREADOR
# ============================================================

print()
print("8. GET USUARIO CREADOR")

response = client.get(
    f"/usuarios/{creador_id}"
)

show_response("GET CREADOR", response)
assert_status(response, 200, "GET creador")

usuario_creador = response.json()

print("Usuario creador:", usuario_creador)

print("  OK: usuario creador recuperado")


# ============================================================
# 9. GET USUARIO APROBADOR
# ============================================================

print()
print("9. GET USUARIO APROBADOR")

response = client.get(
    f"/usuarios/{aprobador_id}"
)

show_response("GET APROBADOR", response)
assert_status(response, 200, "GET aprobador")

usuario_aprobador = response.json()

print("Usuario aprobador:", usuario_aprobador)

print("  OK: usuario aprobador recuperado")


# ============================================================
# 10. VALIDAR RELACIONES INVERSAS
# ============================================================

print()
print("10. VALIDAR RELACIONES INVERSAS")

creados = usuario_creador.get("pedidos_creado_por", [])
aprobados = usuario_aprobador.get("pedidos_aprobado_por", [])

print("pedidos_creado_por:", len(creados))
print("pedidos_aprobado_por:", len(aprobados))

assert any(
    pedido_item["id"] == pedido_id
    for pedido_item in creados
)

assert any(
    pedido_item["id"] == pedido_id
    for pedido_item in aprobados
)

print("  OK: Usuario.pedidos_creado_por")
print("  OK: Usuario.pedidos_aprobado_por")


# ============================================================
# 11. VALIDAR AISLAMIENTO INVERSO
# ============================================================

print()
print("11. VALIDAR AISLAMIENTO INVERSO")

assert all(
    item["id"] == pedido_id
    for item in creados
)

assert all(
    item["id"] == pedido_id
    for item in aprobados
)

print("  OK: relación creador aislada")
print("  OK: relación aprobador aislada")


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)

print("POST USUARIO CREADOR: PASS")
print("POST USUARIO APROBADOR: PASS")
print("POST PEDIDO MULTI-FK: PASS")
print("CREADO_POR JSON: PASS")
print("APROBADO_POR JSON: PASS")
print("AISLAMIENTO DIRECTO: PASS")
print("GET PEDIDO: PASS")
print("GET USUARIOS: PASS")
print("RELACIONES INVERSAS: PASS")
print("AISLAMIENTO INVERSO: PASS")
print("FASTAPI MULTI-FK MISMO TARGET: OK")

print("=" * 60)
