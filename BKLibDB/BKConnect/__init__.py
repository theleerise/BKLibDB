#!/usr/bin/env python3
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass


def get_dbconn(type, username=None, password=None, host=None, port=None, database=None, chain_connection=None):
    """
    Crea y devuelve un motor de conexión a una base de datos utilizando SQLAlchemy.

    Args:
        type (str): Tipo de base de datos. Valores soportados: "ORACLE", "POSTGRESQL", "SQLSERVER", "SQLITE".
        username (str, opcional): Usuario de la base de datos.
        password (str, opcional): Contraseña del usuario.
        host (str, opcional): Dirección del servidor donde se aloja la base de datos.
        port (str, opcional): Puerto del servidor.
        database (str): Nombre de la base de datos.

    Returns:
        sqlalchemy.engine.base.Engine: Motor de conexión a la base de datos.

    Example:
        engine = get_dbconn(
            type="POSTGRESQL",
            username="user",
            password="password",
            host="localhost",
            port="5432",
            database="mydb"
        )
    Note: ORACLE NO ACTIVADO
    """
    
    @dataclass
    class ConnDict:
        username: str = None
        password: str = None
        host: str = None
        port: str = None
        database: str = None

    conn_dict = ConnDict(username, password, host, port, database)
    db_uri = _type_connection(type_db=type.upper(), kwargs=conn_dict, chain_connection=chain_connection)
    engine = create_engine(db_uri)
    return engine


def _type_connection(type_db, chain_connection=None, kwargs=None):
    """
    Genera la URI de conexión para diferentes tipos de bases de datos.

    Args:
        type_db (str): Tipo de base de datos en mayúsculas.
        kwargs (ConnDict): Diccionario con los detalles de conexión.

    Returns:
        str: URI de conexión para SQLAlchemy.

    Raises:
        ValueError: Si el tipo de base de datos no está soportado.

    Example:
        db_uri = _type_connection("POSTGRESQL", conn_dict)
        # Resultado: "postgresql+psycopg2://user:password@localhost:5432/mydb"
    
    Note: ORACLE NO ACTIVADO
    """
    if chain_connection:
        return chain_connection
    
    chain_conn = f"{kwargs.username}:{kwargs.password}@{kwargs.host}:{kwargs.port}/{kwargs.database}"
    
    if type_db == "ORACLE":
        db_uri = f"oracle+oracledb://{chain_conn}"
        
    elif type_db == "POSTGRESQL":
        db_uri = f"postgresql+psycopg2://{chain_conn}"
        
    elif type_db == "SQLSERVER":
        db_uri = f"mssql+pyodbc://{chain_conn}?driver=ODBC+Driver+17+for+SQL+Server"
        
    elif type_db == "SQLITE":
        db_uri = f"sqlite:///{kwargs.database}.db"
        
    else:
        raise ValueError(f"Unsupported database type: {type_db}")
    
    return db_uri


def get_dbsess(type, username=None, password=None, host=None, port=None, database=None, chain_connection=None):
    """
    Crea y devuelve una sesión de base de datos utilizando SQLAlchemy.

    Args:
        type (str): Tipo de base de datos. Valores soportados: "ORACLE", "POSTGRESQL", "SQLSERVER", "SQLITE".
        username (str, opcional): Usuario de la base de datos.
        password (str, opcional): Contraseña del usuario.
        host (str, opcional): Dirección del servidor donde se aloja la base de datos.
        port (str, opcional): Puerto del servidor.
        database (str): Nombre de la base de datos.

    Returns:
        sqlalchemy.orm.session.Session: Sesión para interactuar con la base de datos.

    Example:
        session = get_dbsess(
            type="SQLITE",
            database="test"
        )
        session.execute("SELECT 1")
        
    Note: ORACLE NO ACTIVADO
    """
    
    conn = get_dbconn(type=type, username=username, password=password, host=host, port=port, database=database, chain_connection=chain_connection)
    Session = sessionmaker(bind=conn)
    session = Session()
    return session
