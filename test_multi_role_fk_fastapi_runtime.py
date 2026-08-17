import os

os.environ["DB_DRIVER"] = "sqlite"
os.environ["DB_URL"] = "sqlite:///./multi_role_fk_api_runtime.db"


from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


print("=" * 70)
print("FASTAPI MULTI ROLE FK RUNTIME")
print("=" * 70)


print("\nROUTES")
for route in app.routes:
    if hasattr(route, "path"):
        print(route.path)


print("\nOK IMPORT FASTAPI")
