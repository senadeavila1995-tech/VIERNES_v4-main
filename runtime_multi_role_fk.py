import os

os.environ["DB_DRIVER"] = "sqlite"
os.environ["DB_URL"] = "sqlite:///./multi_role_fk_runtime.db"


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.modules.usuario.models.usuario import Usuario
from backend.modules.pedido.models.pedido import Pedido
from backend.framework.base_model import Base


engine = create_engine(
    os.environ["DB_URL"],
    echo=True,
)


print("=" * 70)
print("CREANDO TABLAS")
print("=" * 70)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(
    bind=engine
)


db = SessionLocal()


print("=" * 70)
print("INSERT USUARIO")
print("=" * 70)


usuario1 = Usuario(
    nombre="Carlos"
)

usuario2 = Usuario(
    nombre="Ana"
)


db.add_all(
    [
        usuario1,
        usuario2,
    ]
)

db.commit()

db.refresh(usuario1)
db.refresh(usuario2)


print(
    "Usuarios:",
    usuario1.id,
    usuario2.id
)


print("=" * 70)
print("INSERT PEDIDO")
print("=" * 70)


pedido = Pedido(
    descripcion="Pedido prueba roles",
    creado_por_id=usuario1.id,
    aprobado_por_id=usuario2.id,
)


db.add(pedido)

db.commit()

db.refresh(pedido)


print(
    "Pedido:",
    pedido.id
)


print("=" * 70)
print("RELACIONES")
print("=" * 70)


print(
    "creado_por:",
    pedido.creado_por.nombre
)


print(
    "aprobado_por:",
    pedido.aprobado_por.nombre
)


print(
    "pedidos creados:",
    len(usuario1.pedidos_creado_por)
)


print(
    "pedidos aprobados:",
    len(usuario2.pedidos_aprobado_por)
)


print("=" * 70)
print("OK RUNTIME MULTI ROLE FK")
print("=" * 70)
