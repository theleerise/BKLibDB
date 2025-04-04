from cassandra.cluster import Cluster
from BKLibDB.BKModel.BKNoSQLModel.Cassandra.CassandraBKModel_Base import CassandraModel

class CassandraManager:
    """
    Manager base para manejar operaciones CRUD en Cassandra con lógica before_ y after_.
    """
    def __init__(self, model, keyspace, table, hosts=["127.0.0.1"]):
        """
        Inicializa la conexión a Cassandra y define el modelo.
        """
        self.model = model
        self.keyspace = keyspace
        self.table = table
        self.cluster = Cluster(hosts)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.cluster.shutdown()

    # --- INSERT ---
    def insert(self, data):
        """
        Inserta un registro en la tabla.
        """
        if hasattr(self, "before_insert"):
            self.before_insert(data)

        columns = ", ".join(data.to_dict().keys())
        placeholders = ", ".join(["%s"] * len(data.to_dict()))
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.session.execute(query, tuple(data.to_dict().values()))

        if hasattr(self, "after_insert"):
            self.after_insert(data)

    def before_insert(self, data):
        print(f"[Before Insert] Preparando para insertar: {data.to_dict()}")

    def after_insert(self, data):
        print(f"[After Insert] Registro insertado correctamente: {data.to_dict()}")

    # --- UPDATE ---
    def update(self, condition, updates):
        """
        Actualiza registros en la tabla.
        """
        if hasattr(self, "before_update"):
            self.before_update(condition, updates)

        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"UPDATE {self.table} SET {set_clause} WHERE {condition}"
        self.session.execute(query, tuple(updates.values()))

        if hasattr(self, "after_update"):
            self.after_update(condition, updates)

    def before_update(self, condition, updates):
        print(f"[Before Update] Preparando para actualizar: {updates} con condición: {condition}")

    def after_update(self, condition, updates):
        print(f"[After Update] Registros actualizados correctamente: {updates}")

    # --- DELETE ---
    def delete(self, condition):
        """
        Elimina registros que cumplan la condición.
        """
        if hasattr(self, "before_delete"):
            self.before_delete(condition)

        query = f"DELETE FROM {self.table} WHERE {condition}"
        self.session.execute(query)

        if hasattr(self, "after_delete"):
            self.after_delete(condition)

    def before_delete(self, condition):
        print(f"[Before Delete] Preparando para eliminar registros con condición: {condition}")

    def after_delete(self, condition):
        print(f"[After Delete] Registros eliminados correctamente con condición: {condition}")

    # --- FIND ---
    def find(self, condition=None):
        """
        Recupera registros de la tabla.
        """
        query = f"SELECT * FROM {self.table}"
        if condition:
            query += f" WHERE {condition}"

        rows = self.session.execute(query)
        return [self.model.from_row(row) for row in rows]


if __name__ == "__main__":
    """
from CassandraModel import CassandraModel
from CassandraManager import CassandraManager

# Definir un modelo específico heredando de CassandraModel
class Usuario(CassandraModel):
    def __init__(self, id, nombre, edad, correo):
        super().__init__(id=id, nombre=nombre, edad=edad, correo=correo)

# Inicializar el manager
manager = CassandraManager(model=Usuario, keyspace="testkeyspace", table="usuarios", hosts=["127.0.0.1"])

# Crear un modelo
usuario = Usuario(id=1, nombre="Elieser", edad=30, correo="elieser@example.com")

# Insertar un registro
manager.insert(usuario)

# Actualizar registros
manager.update("id = 1", {"edad": 31, "correo": "elieser@nuevo.com"})

# Buscar registros
resultados = manager.find("edad >= 30")
for usuario in resultados:
    print(usuario.to_dict())

# Eliminar registros
manager.delete("id = 1")

# Cerrar conexión
manager.close()

    """