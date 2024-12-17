class MongoDBModel:
    """
    Modelo base para representar un documento de MongoDB como objeto.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        """
        Crea un modelo desde un diccionario.
        """
        return cls(**data)

    def to_dict(self):
        """
        Convierte el modelo a un diccionario.
        """
        return self.__dict__
