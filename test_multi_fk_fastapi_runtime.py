"""
REGRESIÓN — FASTAPI REAL / MULTI-FK

Valida el CRUD generado a través de HTTP usando TestClient.

Contrato:

Categoria
   |
   +---- Producto
   |
   +---- DetalleProducto
             |
             +---- Producto

Producto -> DetalleProducto
    ON DELETE CASCADE

Categoria -> DetalleProducto
    ON DELETE RESTRICT
"""

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def show(label, response):
    print()
    print(f"=== {label} ===")
    print("STATUS:", response.status_code)
    print("BODY:", response.text[:2000])


print("=" * 60)
print("RUNTIME FASTAPI — MULTI-FK")
print("=" * 60)


# ============================================================
# 1. CATEGORIA
# ============================================================

print()
print("1. CREAR CATEGORIA")

response = client.post(
    "/categoria/",
    json={
        "nombre": "FASTAPI_MULTI_FK"
    },
)

show("CREATE CATEGORIA", response)

assert response.status_code == 200, response.text

categoria = response.json()
categoria_id = categoria["id"]

print("Categoria ID:", categoria_id)


# ============================================================
# 2. PRODUCTO
# ============================================================

print()
print("2. CREAR PRODUCTO")

response = client.post(
    "/producto/",
    json={
        "nombre": "FASTAPI_PRODUCTO",
        "categoria_id": categoria_id,
    },
)

show("CREATE PRODUCTO", response)

assert response.status_code == 200, response.text

producto = response.json()
producto_id = producto["id"]

assert producto["categoria_id"] == categoria_id

print("Producto ID:", producto_id)


# ============================================================
# 3. DETALLE
# ============================================================

print()
print("3. CREAR DETALLE")

response = client.post(
    "/detalle_producto/",
    json={
        "cantidad": 25,
        "producto_id": producto_id,
        "categoria_id": categoria_id,
    },
)

show("CREATE DETALLE", response)

assert response.status_code == 200, response.text

detalle = response.json()
detalle_id = detalle["id"]

assert detalle["producto_id"] == producto_id
assert detalle["categoria_id"] == categoria_id

print("Detalle ID:", detalle_id)


# ============================================================
# 4. VERIFICAR RELACIONES
# ============================================================

print()
print("4. VERIFICAR RELACIONES")

assert detalle["producto"]["id"] == producto_id
assert detalle["categoria"]["id"] == categoria_id

print("  OK: detalle.producto")
print("  OK: detalle.categoria")
print("  OK: ambas relaciones presentes")


# ============================================================
# 5. DELETE PRODUCTO
# ============================================================

print()
print("5. DELETE PRODUCTO — CASCADE")

response = client.delete(
    f"/producto/{producto_id}"
)

show("DELETE PRODUCTO", response)

assert response.status_code == 200, response.text

print("  OK: Producto eliminado")


# ============================================================
# 6. DETALLE DEBE DESAPARECER
# ============================================================

print()
print("6. VERIFICAR CASCADE")

response = client.get(
    f"/detalle_producto/{detalle_id}"
)

show("GET DETALLE DESPUÉS DE CASCADE", response)

assert response.status_code == 404, response.text

print("  OK: DetalleProducto eliminado por CASCADE")


# ============================================================
# 7. CREAR SEGUNDO PRODUCTO
# ============================================================

print()
print("7. CREAR SEGUNDO PRODUCTO")

response = client.post(
    "/producto/",
    json={
        "nombre": "FASTAPI_RESTRICT_PRODUCTO",
        "categoria_id": categoria_id,
    },
)

show("CREATE SEGUNDO PRODUCTO", response)

assert response.status_code == 200, response.text

producto2 = response.json()
producto2_id = producto2["id"]

print("Producto ID:", producto2_id)


# ============================================================
# 8. CREAR SEGUNDO DETALLE
# ============================================================

print()
print("8. CREAR SEGUNDO DETALLE")

response = client.post(
    "/detalle_producto/",
    json={
        "cantidad": 50,
        "producto_id": producto2_id,
        "categoria_id": categoria_id,
    },
)

show("CREATE SEGUNDO DETALLE", response)

assert response.status_code == 200, response.text

detalle2 = response.json()
detalle2_id = detalle2["id"]

print("Detalle ID:", detalle2_id)


# ============================================================
# 9. DELETE CATEGORIA
# ============================================================

print()
print("9. DELETE CATEGORIA — RESTRICT")

response = client.delete(
    f"/categoria/{categoria_id}"
)

show("DELETE CATEGORIA", response)

assert response.status_code == 409, response.text

print("  OK: Categoria protegida por RESTRICT")


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 60)
print("RESULTADO FINAL")
print("=" * 60)
print("POST CATEGORIA: PASS")
print("POST PRODUCTO: PASS")
print("POST DETALLE: PASS")
print("RELACIONES JSON: PASS")
print("CASCADE: PASS")
print("RESTRICT: PASS")
print("FASTAPI RUNTIME REFERENCIAL: OK")
print("=" * 60)
