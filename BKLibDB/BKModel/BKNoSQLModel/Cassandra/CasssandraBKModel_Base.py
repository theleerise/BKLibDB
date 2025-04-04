class CassandraModel:
    """
    Modelo base para representar filas de Cassandra como objetos.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_row(cls, row):
        """
        Crea un modelo a partir de una fila de Cassandra.
        """
        return cls(**row._asdict())

    def to_dict(self):
        """
        Convierte el modelo a un diccionario.
        """
        return self.__dict__
