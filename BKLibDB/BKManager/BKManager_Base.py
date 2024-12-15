#!/usr/bin/env python3
# coding: utf-8

from sqlalchemy.sql import text
from BKLibDB.BKConnect import get_dbsess  # Para abrir sesiones


class BKManager:
    """
    Manager base para manejar operaciones SQL y CRUD en la base de datos.
    Los managers específicos pueden sobrescribir consultas y lógica.
    """
    def __init__(self, session=None, model=None):
        """
        Inicializa BKManager con una sesión de base de datos y un modelo opcional.

        Args:
            session (sqlalchemy.orm.session.Session, opcional): Sesión de la base de datos.
            model (class, opcional): Modelo asociado al manager.
        """
        self.session = session
        self.model = model

    def open_session(self, db_type, **kwargs):
        """
        Abre una nueva sesión con la base de datos.

        Args:
            db_type (str): Tipo de base de datos (e.g., "SQLITE", "POSTGRESQL").
            kwargs (dict): Parámetros de conexión.

        Returns:
            sqlalchemy.orm.session.Session: Sesión abierta.
        """
        return get_dbsess(type=db_type, **kwargs)

    def execute_query(self, sql, params=None):
        """
        Ejecuta una consulta SQL genérica.
    
        Args:
            sql (str): Sentencia SQL.
            params (dict, opcional): Parámetros de la consulta.
    
        Returns:
            list[dict]: Resultados de la consulta como una lista de diccionarios.
        """
        result = self.session.execute(text(sql), params or {})
        return [row._asdict() for row in result]  # Usa _asdict() para convertir Row en dict
    

    def fetch_all(self, sql, params=None):
        """
        Ejecuta una consulta SQL y mapea los resultados al modelo.

        Args:
            sql (str): Sentencia SQL.
            params (dict, opcional): Parámetros de la consulta.

        Returns:
            list[model]: Lista de instancias del modelo con los datos mapeados.
        """
        if not self.model:
            raise ValueError("No se ha definido un modelo para este manager.")
        results = self.execute_query(sql, params)
        return self.model.from_query(results)

    def insert(self, sql, params):
        """
        Ejecuta una inserción en la base de datos.

        Args:
            sql (str): Sentencia SQL de inserción.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        # Llamar a before_insert si está definido
        if hasattr(self, "before_insert"):
            self.before_insert(params)

        result = self.session.execute(text(sql), params)
        self.session.commit()

        # Llamar a after_insert si está definido
        if hasattr(self, "after_insert"):
            self.after_insert(params)

        return result.rowcount

    def update(self, sql, params):
        """
        Ejecuta una actualización en la base de datos.

        Args:
            sql (str): Sentencia SQL de actualización.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        # Llamar a before_update si está definido
        if hasattr(self, "before_update"):
            self.before_update(params)

        result = self.session.execute(text(sql), params)
        self.session.commit()

        # Llamar a after_update si está definido
        if hasattr(self, "after_update"):
            self.after_update(params)

        return result.rowcount

    def delete(self, sql, params):
        """
        Ejecuta un borrado en la base de datos.

        Args:
            sql (str): Sentencia SQL de borrado.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        # Llamar a before_delete si está definido
        if hasattr(self, "before_delete"):
            self.before_delete(params)

        result = self.session.execute(text(sql), params)
        self.session.commit()

        # Llamar a after_delete si está definido
        if hasattr(self, "after_delete"):
            self.after_delete(params)

        return result.rowcount
