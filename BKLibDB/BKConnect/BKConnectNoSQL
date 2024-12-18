#!/usr/bin/env python3
# coding: utf-8

from pymongo import MongoClient
from redis import Redis
from cassandra.cluster import Cluster
from neo4j import GraphDatabase

class BKConnectNoSQL:
    """
    Clase para manejar conexiones a bases de datos NoSQL.
    Proporciona soporte para MongoDB, Redis, Cassandra y Neo4j.
    """

    def __init__(self, db_type, **kwargs):
        """
        Inicializa la conexión a una base de datos NoSQL.

        Args:
            db_type (str): Tipo de base de datos ("MONGO", "REDIS", "CASSANDRA", "NEO4J").
            kwargs (dict): Parámetros de conexión específicos según el tipo de base de datos.
        """
        self.db_type = db_type.upper()
        self.connection = self._connect(db_type=self.db_type, **kwargs)

    def _connect(self, db_type, **kwargs):
        """
        Establece la conexión a la base de datos NoSQL especificada.

        Args:
            db_type (str): Tipo de base de datos ("MONGO", "REDIS", "CASSANDRA", "NEO4J").
            kwargs (dict): Parámetros de conexión.

        Returns:
            object: Conexión al cliente de la base de datos.
        """
        if db_type == "MONGO":
            return MongoClient(kwargs.get("host", "localhost"), kwargs.get("port", 27017))
        elif db_type == "REDIS":
            return Redis(host=kwargs.get("host", "localhost"), port=kwargs.get("port", 6379))
        elif db_type == "CASSANDRA":
            cluster = Cluster(kwargs.get("hosts", ["localhost"]))
            return cluster.connect(kwargs.get("keyspace"))
        elif db_type == "NEO4J":
            uri = f"bolt://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 7687)}"
            return GraphDatabase.driver(uri, auth=(kwargs.get("username"), kwargs.get("password")))
        else:
            raise ValueError(f"Unsupported NoSQL database type: {db_type}")

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.db_type == "MONGO":
            self.connection.close()
        elif self.db_type == "REDIS":
            self.connection.close()
        elif self.db_type == "CASSANDRA":
            self.connection.cluster.shutdown()
            self.connection.shutdown()
        elif self.db_type == "NEO4J":
            self.connection.close()
        else:
            raise ValueError(f"Unsupported NoSQL database type: {self.db_type}")

    def get_connection(self):
        """
        Devuelve el cliente o sesión activa.

        Returns:
            object: Conexión activa a la base de datos.
        """
        return self.connection
