from pymongo import MongoClient
from BKLibDB.BKModel.BKNoSQLModel.Mongo.MongoBKModel_Base import MongoDBModel


class MongoDBManager:
    """
    Manager base para manejar operaciones CRUD en MongoDB con lógica before_ y after_.
    """
    def __init__(self, model, database, collection, host="localhost", port=27017):
        """
        Inicializa la conexión a MongoDB y selecciona la base de datos y colección.
        """
        self.model = model
        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.collection = self.db[collection]

    # --- INSERT ---
    def insert(self, model):
        """
        Inserta un documento en la colección.
        """
        if hasattr(self, "before_insert"):
            self.before_insert(model)
        result = self.collection.insert_one(model.to_dict())
        if hasattr(self, "after_insert"):
            self.after_insert(model)
        return result.inserted_id

    def before_insert(self, model):
        print(f"[Before Insert] Preparando para insertar: {model.to_dict()}")

    def after_insert(self, model):
        print(f"[After Insert] Documento insertado correctamente: {model.to_dict()}")

    # --- UPDATE ---
    def update(self, query, new_data):
        """
        Actualiza documentos que coincidan con la condición.
        """
        if hasattr(self, "before_update"):
            self.before_update(query, new_data)
        result = self.collection.update_many(query, {"$set": new_data})
        if hasattr(self, "after_update"):
            self.after_update(query, new_data)
        return result.modified_count

    def before_update(self, query, new_data):
        print(f"[Before Update] Condición: {query}, Datos a actualizar: {new_data}")

    def after_update(self, query, new_data):
        print(f"[After Update] Actualización completada. Condición: {query}, Nuevos datos: {new_data}")

    # --- DELETE ---
    def delete(self, query):
        """
        Elimina documentos que coincidan con la condición.
        """
        if hasattr(self, "before_delete"):
            self.before_delete(query)
        result = self.collection.delete_many(query)
        if hasattr(self, "after_delete"):
            self.after_delete(query)
        return result.deleted_count

    def before_delete(self, query):
        print(f"[Before Delete] Preparando para eliminar documentos que coinciden con: {query}")

    def after_delete(self, query):
        print(f"[After Delete] Documentos eliminados con la condición: {query}")

    # --- FIND ---
    def find(self, query=None):
        """
        Busca documentos en la colección que coincidan con la condición.
        """
        results = self.collection.find(query or {})
        return [self.model.from_dict(doc) for doc in results]


if __name__ == "__main__":
    """
from MongoDBModel import MongoDBModel
from MongoDBManager import MongoDBManager

# Definir el modelo
class Usuario(MongoDBModel):
    def __init__(self, nombre, edad, correo):
        super().__init__(nombre=nombre, edad=edad, correo=correo)

# Inicializar el manager con el modelo Usuario
manager = MongoDBManager(model=Usuario, database="testdb", collection="usuarios")

# Crear un modelo
usuario = Usuario(nombre="Elieser", edad=30, correo="elieser@example.com")

# Insertar un documento
manager.insert(usuario)

# Actualizar documentos
manager.update({"nombre": "Elieser"}, {"edad": 31})

# Eliminar documentos
manager.delete({"nombre": "Elieser"})

# Buscar documentos
resultados = manager.find()
for usuario in resultados:
    print(usuario.to_dict())

    """