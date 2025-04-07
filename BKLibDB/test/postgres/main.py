from MgrdbTest import MgrdbTest

if __name__ == "__main__":
    # Conexión a PostgreSQL
    manager = MgrdbTest(
        db_type="POSTGRESQL",
        username="postgres",
        password="",
        host="localhost",
        port="5432",
        database="postgres"
    )

    resultado = manager.fetch_all(manager.get_sql_select(), {"id": 1})
    print("Resultado:", resultado)
