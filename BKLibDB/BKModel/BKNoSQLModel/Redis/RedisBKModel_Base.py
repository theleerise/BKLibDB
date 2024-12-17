import json

class RedisModel:
    """
    Modelo base para representar datos en Redis como objetos.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self):
        """
        Convierte el modelo a JSON.
        """
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_data):
        """
        Crea un modelo desde JSON.
        """
        return cls(**json.loads(json_data))
