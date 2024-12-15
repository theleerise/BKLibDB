#!/usr/bin/env python3
# coding: utf-8

class BKColumn:
    """
    Representa una columna personalizada que define metadatos y mapea datos de consultas.
    """
    def __init__(self, name, coltype, nullable=True, primary_key=False, doc=None, fk=None):
        self.name = name
        self.coltype = coltype
        self.nullable = nullable
        self.primary_key = primary_key
        self.doc = doc
        self.fk = fk


class BKModel:
    """
    Clase base para modelos que no dependen directamente de tablas de la base de datos.
    Es flexible y permite crear objetos con datos de consultas personalizadas.
    """
    def __init__(self, **kwargs):
        """
        Inicializa el modelo con los valores proporcionados.

        Args:
            kwargs (dict): Datos de inicialización, donde cada clave es un atributo del modelo.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """
        Representación del modelo, mostrando sus atributos.
        """
        attrs = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"<{self.__class__.__name__}({attrs})>"

    @classmethod
    def from_query(cls, results):
        """
        Convierte resultados de consultas (lista de diccionarios) en una lista de modelos.

        Args:
            results (list[dict]): Lista de diccionarios con los datos de la consulta.

        Returns:
            list[BKModel]: Lista de instancias del modelo con los datos mapeados.
        """
        return [cls(**row) for row in results]

    @staticmethod
    def to_dict(data):
        """
        Convierte un modelo o una lista de modelos en un diccionario o lista de diccionarios.

        Args:
            data (BKModel | list[BKModel]): Modelo o lista de modelos.

        Returns:
            dict | list[dict]: Diccionario o lista de diccionarios.
        """
        if isinstance(data, list):
            return [obj.__dict__ for obj in data]
        return data.__dict__

    @classmethod
    def ensure_list(cls, results):
        """
        Convierte resultados de consultas en una lista de modelos, aunque sea un solo resultado.

        Args:
            results (list[dict] | dict): Resultados de la consulta.

        Returns:
            list[BKModel]: Lista de modelos.
        """
        if isinstance(results, dict):
            results = [results]
        return cls.from_query(results)
