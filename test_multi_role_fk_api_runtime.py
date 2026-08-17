import os

os.environ["DB_DRIVER"] = "sqlite"
os.environ["DB_URL"] = "sqlite:///./multi_role_fk_api_runtime.db"


from fastapi.testclient import TestClient

from backend.main import app


print("=" * 70)
print("API MULTI ROLE FK RUNTIME")
print("=" * 70)


with TestClient(app) as client:

    print("\nCREAR USUARIOS")

    carlos = client.post(
        "/usuario/",
        json={
            "nombre": "Carlos"
        },
    )

    ana = client.post(
        "/usuario/",
        json={
            "nombre": "Ana"
        },
    )


    print("CARLOS:", carlos.status_code, carlos.json())
    print("ANA:", ana.status_code, ana.json())


    carlos_id = carlos.json()["id"]
    ana_id = ana.json()["id"]


    print("\nCREAR PEDIDO")

    pedido = client.post(
        "/pedido/",
        json={
            "descripcion": "Pedido multi role",
            "creado_por_id": carlos_id,
            "aprobado_por_id": ana_id,
        },
    )


    print(
        "PEDIDO:",
        pedido.status_code,
        pedido.json()
    )


    print("\nOBTENER PEDIDO")

    response = client.get(
        f"/pedido/{pedido.json()['id']}"
    )


    print(
        "GET PEDIDO:",
        response.status_code,
        response.json()
    )


    print("\nLISTAR PEDIDOS")

    response = client.get(
        "/pedido/"
    )

    print(
        "LIST:",
        response.status_code,
        response.json()
    )


print("\nOK API MULTI ROLE FK COMPLETA")
