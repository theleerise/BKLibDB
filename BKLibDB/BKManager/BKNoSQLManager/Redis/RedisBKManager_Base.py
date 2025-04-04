import redis
from BKLibDB.BKModel.BKNoSQLModel.Redis.RedisBKModel_Base import RedisModel

class RedisManager:
    """
    Manager base para manejar operaciones CRUD en Redis con lógica before_ y after_.
    """
    def __init__(self, model, host="localhost", port=6379, db=0):
        """
        Inicializa la conexión con Redis y define el modelo.
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self.model = model

    # --- INSERT ---
    def insert(self, key, model):
        """
        Inserta un modelo en Redis.
        """
        if hasattr(self, "before_insert"):
            self.before_insert(key, model)
        self.client.set(key, model.to_json())
        if hasattr(self, "after_insert"):
            self.after_insert(key, model)

    def before_insert(self, key, model):
        print(f"[Before Insert] Preparando para insertar clave '{key}' con valor: {model.to_json()}")

    def after_insert(self, key, model):
        print(f"[After Insert] Clave '{key}' insertada correctamente.")

    # --- UPDATE ---
    def update(self, key, new_data):
        """
        Actualiza un modelo existente en Redis.
        """
        if hasattr(self, "before_update"):
            self.before_update(key, new_data)
        existing = self.client.get(key)
        if existing:
            model_data = RedisModel.from_json(existing)
            model_data.__dict__.update(new_data)
            self.client.set(key, model_data.to_json())
            if hasattr(self, "after_update"):
                self.after_update(key, new_data)
        else:
            print(f"[Update] Clave '{key}' no encontrada.")

    def before_update(self, key, new_data):
        print(f"[Before Update] Preparando para actualizar clave '{key}' con datos: {new_data}")

    def after_update(self, key, new_data):
        print(f"[After Update] Clave '{key}' actualizada correctamente con datos: {new_data}")

    # --- DELETE ---
    def delete(self, key):
        """
        Elimina un modelo en Redis.
        """
        if hasattr(self, "before_delete"):
            self.before_delete(key)
        self.client.delete(key)
        if hasattr(self, "after_delete"):
            self.after_delete(key)

    def before_delete(self, key):
        print(f"[Before Delete] Preparando para eliminar clave '{key}'.")

    def after_delete(self, key):
        print(f"[After Delete] Clave '{key}' eliminada correctamente.")

    # --- FIND ---
    def find(self, key):
        """
        Busca un modelo en Redis por su clave.
        """
        data = self.client.get(key)
        if data:
            return self.model.from_json(data)
        return None

if __name__ == "__main__":
    """
from RedisModel import RedisModel
from RedisManager import RedisManager

# Definir un modelo específico heredando de RedisModel
class Usuario(RedisModel):
    def __init__(self, nombre, edad, correo):
        super().__init__(nombre=nombre, edad=edad, correo=correo)

# Inicializar el manager con el modelo Usuario
manager = RedisManager(model=Usuario, host="localhost", port=6379)

# Crear un modelo
usuario = Usuario(nombre="Elieser", edad=30, correo="elieser@example.com")

# Insertar un modelo
manager.insert("usuario:1", usuario)

# Actualizar un modelo
manager.update("usuario:1", {"edad": 31, "correo": "elieser@nuevo.com"})

# Buscar un modelo
resultado = manager.find("usuario:1")
if resultado:
    print("Usuario encontrado:", resultado.__dict__)

# Eliminar un modelo
manager.delete("usuario:1")

    """