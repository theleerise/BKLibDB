#!/usr/bin/env python3
# coding: utf-8

from BKLibDB.BKManager.BKManager_Base import BKManager
from abc import ABC, abstractmethod
from sqlalchemy.sql import text


class BKManagerDB(BKManager):
    """
    Manager para bases de datos relacionales que extiende BKManager
    y agrega manejo automático de finalización y transacciones.
    """

    def __init__(self, model=None, db_type=None, session=None, chain_connection=None, **kwargs):
        """
        Inicializa BKManagerDB con una sesión activa y un modelo opcional.

        Args:
            session (sqlalchemy.orm.session.Session, opcional): Sesión de la base de datos.
            model (class, opcional): Modelo asociado al manager.
        """
        ### Si no se pasa una sesión explícita, intenta crearla con los parámetros.
        if session is None and db_type:
            session = self.open_session(db_type=db_type, chain_connection=chain_connection, **kwargs)
        
        super().__init__(session=session, model=model)

    def __enter__(self):
        """
        Permite usar el manager como un context manager.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cierra la sesión automáticamente al salir del bloque `with`.
        Si ocurre un error, revierte la transacción; de lo contrario, la confirma.
        """
        if self.session:
            if exc_type is not None:
                self.session.rollback()  # Revertir transacción en caso de error
            else:
                self.session.commit()  # Confirmar transacción si no hay errores
            self.session.close()  # Cerrar la sesión en cualquier caso
    
    @abstractmethod
    def get_sql_query(self):
        """
        Debe devolver una tupla (sql: str, params: dict) para consultas SELECT.
        """
        pass

    @abstractmethod
    def get_sql_insert(self):
        """
        Debe devolver una tupla (sql: str, params: dict) para INSERT.
        """
        pass

    @abstractmethod
    def get_sql_update(self):
        """
        Debe devolver una tupla (sql: str, params: dict) para UPDATE.
        """
        pass

    @abstractmethod
    def get_sql_delete(self):
        """
        Debe devolver una tupla (sql: str, params: dict) para DELETE.
        """
        pass

    # CRUD con manejo implícito de transacciones y hooks
    def getlist(self):
        """
        Ejecuta una consulta SELECT genérica usando get_sql_query.
    
        Returns:
            list[BKModel]: Lista de instancias del modelo con los datos obtenidos.
        """
        try:
            sql, params = self.get_sql_select()
            return self.fetch_all(sql, params)
        except Exception as e:
            self.session.rollback()  # En caso de error, revierte la transacción
            raise e
    
    def insert(self, sql=None, params=None, objmodel=None):
        """
        Ejecuta una inserción con manejo automático de transacciones.

        Args:
            sql (str): Sentencia SQL de inserción.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        if sql is None or params is None and objmodel is None:
            sql, params = self.get_sql_insert()
        if objmodel:
            sql, _ = self.get_sql_insert()
            params = objmodel.to_dict()
            
        try:
            if hasattr(self, "before_insert"):
                self.before_insert(params)  # Hook antes de la inserción
            rowcount = super().insert(sql, params)
            self.session.commit()  # Confirmar transacción tras la inserción exitosa
            if hasattr(self, "after_insert"):
                self.after_insert(params)  # Hook después de la inserción
            return rowcount
        except Exception as e:
            self.session.rollback()  # Revertir transacción en caso de error
            raise e

    def update(self, sql=None, params=None, objmodel=None):
        """
        Ejecuta una actualización con manejo automático de transacciones.

        Args:
            sql (str): Sentencia SQL de actualización.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        if sql is None or params is None and objmodel is None:
            sql, params = self.get_sql_update()
        if objmodel:
            sql, _ = self.get_sql_update()
            params = objmodel.to_dict()
            
        try:
            if hasattr(self, "before_update"):
                self.before_update(params)  # Hook antes de la actualización
            rowcount = super().update(sql, params)
            self.session.commit()  # Confirmar transacción tras la actualización exitosa
            if hasattr(self, "after_update"):
                self.after_update(params)  # Hook después de la actualización
            return rowcount
        except Exception as e:
            self.session.rollback()  # Revertir transacción en caso de error
            raise e

    def delete(self, sql=None, params=None, objmodel=None):
        """
        Ejecuta un borrado con manejo automático de transacciones.

        Args:
            sql (str): Sentencia SQL de borrado.
            params (dict): Parámetros de la consulta.

        Returns:
            int: Número de filas afectadas.
        """
        if sql is None or params is None and objmodel is None:
            sql, params = self.get_sql_delete()
        if objmodel:
            sql, _ = self.get_sql_delete()
            params = objmodel.to_dict()
                        
        try:
            if hasattr(self, "before_delete"):
                self.before_delete(params)  # Hook antes del borrado
            rowcount = super().delete(sql, params)
            self.session.commit()  # Confirmar transacción tras el borrado exitoso
            if hasattr(self, "after_delete"):
                self.after_delete(params)  # Hook después del borrado
            return rowcount
        except Exception as e:
            self.session.rollback()  # Revertir transacción en caso de error
            raise e

    # Métodos CRUD genéricos
    def execute_query(self, sql, params=None):
        """
        Ejecuta una consulta SQL genérica con manejo automático de transacciones.

        Args:
            sql (str): Sentencia SQL.
            params (dict, opcional): Parámetros de la consulta.

        Returns:
            list[dict]: Resultados de la consulta como una lista de diccionarios.
        """
        try:
            result = super().execute_query(sql, params)
            self.session.commit()  # Confirmar transacción tras la ejecución exitosa
            return result
        except Exception as e:
            self.session.rollback()  # Revertir transacción en caso de error
            raise e

    # Hooks (opcionalmente definidos en los managers específicos)
    def before_insert(self, params):
        """
        Lógica personalizada antes de una operación de inserción.
        Sobrescribir en subclases según sea necesario.
        """
        pass

    def after_insert(self, params):
        """
        Lógica personalizada después de una operación de inserción.
        Sobrescribir en subclases según sea necesario.
        """
        pass

    def before_update(self, params):
        """
        Lógica personalizada antes de una operación de actualización.
        Sobrescribir en subclases según sea necesario.
        """
        pass

    def after_update(self, params):
        """
        Lógica personalizada después de una operación de actualización.
        Sobrescribir en subclases según sea necesario.
        """
        pass

    def before_delete(self, params):
        """
        Lógica personalizada antes de una operación de borrado.
        Sobrescribir en subclases según sea necesario.
        """
        pass

    def after_delete(self, params):
        """
        Lógica personalizada después de una operación de borrado.
        Sobrescribir en subclases según sea necesario.
        """
        pass
    
    def call_procedure(self, proc_name, params=None):
        """
        Ejecuta un procedimiento almacenado adaptándose al tipo de base de datos.

        Args:
            proc_name (str): Nombre del procedimiento.
            params (dict, opcional): Parámetros a pasar.

        Returns:
            None
        """
        params = params or {}
        placeholders = ', '.join(f':{k}' for k in params.keys())

        if self.db_type == "ORACLE":
            sql = f"BEGIN {proc_name}({placeholders}); END;"
        elif self.db_type == "POSTGRESQL":
            sql = f"CALL {proc_name}({placeholders});"
        elif self.db_type == "SQLSERVER":
            sql = f"EXEC {proc_name} " + ', '.join(f"@{k} = :{k}" for k in params.keys())
        elif self.db_type == "MYSQL":
            sql = f"CALL {proc_name}({placeholders});"
        else:
            raise NotImplementedError(f"call_procedure no implementado para {self.db_type}")

        self.session.execute(text(sql), params)
        self.session.commit()
    
    def call_function(self, func_name, params=None):
        """
        Ejecuta una función almacenada y retorna su resultado, adaptándose al tipo de base de datos.
    
        Args:
            func_name (str): Nombre de la función.
            params (dict, opcional): Parámetros a pasar.
    
        Returns:
            Cualquier valor retornado por la función.
        """
        params = params or {}
        placeholders = ', '.join(f':{k}' for k in params.keys())
    
        if self.db_type == "ORACLE":
            sql = f"SELECT {func_name}({placeholders}) AS result FROM DUAL"
        elif self.db_type == "POSTGRESQL":
            sql = f"SELECT {func_name}({placeholders}) AS result"
        elif self.db_type == "SQLSERVER":
            sql = f"SELECT dbo.{func_name}({placeholders}) AS result"
        elif self.db_type == "MYSQL":
            sql = f"SELECT {func_name}({placeholders}) AS result"
        else:
            raise NotImplementedError(f"call_function no implementado para {self.db_type}")
    
        result = self.session.execute(text(sql), params)
        return result.scalar()
    
    def call_function_multi(self, func_name, params=None):
        """
        Ejecuta una función que retorna múltiples columnas/filas.
    
        Args:
            func_name (str): Nombre de la función.
            params (dict, opcional): Parámetros.
    
        Returns:
            list[dict]: Lista de resultados como diccionarios.
        """
        params = params or {}
        placeholders = ', '.join(f':{k}' for k in params)
    
        if self.db_type == "ORACLE":
            sql = f"SELECT * FROM TABLE({func_name}({placeholders}))"
        elif self.db_type == "POSTGRESQL":
            sql = f"SELECT * FROM {func_name}({placeholders})"
        elif self.db_type == "SQLSERVER":
            # sql = f"SELECT * FROM dbo.{func_name}({placeholders})"
            sql = f"SELECT * FROM {self.schema}.{func_name}({placeholders})"
        else:
            raise NotImplementedError(f"call_function_multi no implementado para {self.db_type}")
    
        result = self.session.execute(text(sql), params)
        return [row._asdict() for row in result]
