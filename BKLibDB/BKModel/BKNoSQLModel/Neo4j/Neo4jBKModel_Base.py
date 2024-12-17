class Neo4jModel:
    """
    Modelo base para representar nodos de Neo4j como objetos.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        """
        Crea un modelo a partir de un diccionario.
        """
        return cls(**data)

    def to_dict(self):
        """
        Convierte el modelo a un diccionario.
        """
        return self.__dict__
