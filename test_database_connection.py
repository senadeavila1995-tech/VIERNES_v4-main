from sqlalchemy import text

from agents.framework.database.connection import engine


def main():
    print("==============================================")
    print("VIERNES - PRUEBA DE CONEXION MYSQL")
    print("==============================================")

    print("Engine:", engine.dialect.name)
    print("Driver:", engine.dialect.driver)

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

            print()
            print("CONEXION MYSQL: OK")
            print("SELECT 1:", value)
            print()
            print("==============================================")

    except Exception as exc:
        print()
        print("CONEXION MYSQL: ERROR")
        print(type(exc).__name__)
        print(exc)
        print()
        print("==============================================")

        raise


if __name__ == "__main__":
    main()
