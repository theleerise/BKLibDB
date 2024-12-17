from neo4j import GraphDatabase
from BKLibDB.BKModel.BKNoSQLModel.Neo4j.Neo4jBKModel_Base import Neo4jModel

class Neo4jManager:
    """
    Manager base para manejar operaciones CRUD en Neo4j con lógica before_ y after_.
    """
    def __init__(self, model, uri, user, password):
        """
        Inicializa la conexión a Neo4j y define el modelo.
        """
        self.model = model
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.driver.close()

    # --- INSERT ---
    def insert(self, label, properties):
        """
        Inserta un nodo en la base de datos.
        """
        if hasattr(self, "before_insert"):
            self.before_insert(label, properties)

        query = f"CREATE (n:{label} $props)"
        with self.driver.session() as session:
            session.run(query, props=properties)

        if hasattr(self, "after_insert"):
            self.after_insert(label, properties)

    def before_insert(self, label, properties):
        print(f"[Before Insert] Preparando para insertar nodo '{label}' con propiedades: {properties}")

    def after_insert(self, label, properties):
        print(f"[After Insert] Nodo '{label}' insertado correctamente con propiedades: {properties}")

    # --- UPDATE ---
    def update(self, label, match_condition, new_data):
        """
        Actualiza nodos que cumplan la condición.
        """
        if hasattr(self, "before_update"):
            self.before_update(label, match_condition, new_data)

        query = f"""
        MATCH (n:{label}) WHERE {match_condition}
        SET n += $props
        """
        with self.driver.session() as session:
            session.run(query, props=new_data)

        if hasattr(self, "after_update"):
            self.after_update(label, match_condition, new_data)

    def before_update(self, label, match_condition, new_data):
        print(f"[Before Update] Preparando para actualizar nodos '{label}' que coincidan con: {match_condition}, Nuevos datos: {new_data}")

    def after_update(self, label, match_condition, new_data):
        print(f"[After Update] Nodos '{label}' actualizados correctamente con datos: {new_data}")

    # --- DELETE ---
    def delete(self, label, match_condition):
        """
        Elimina nodos que cumplan la condición.
        """
        if hasattr(self, "before_delete"):
            self.before_delete(label, match_condition)

        query = f"""
        MATCH (n:{label}) WHERE {match_condition}
        DETACH DELETE n
        """
        with self.driver.session() as session:
            session.run(query)

        if hasattr(self, "after_delete"):
            self.after_delete(label, match_condition)

    def before_delete(self, label, match_condition):
        print(f"[Before Delete] Preparando para eliminar nodos '{label}' que coincidan con: {match_condition}")

    def after_delete(self, label, match_condition):
        print(f"[After Delete] Nodos '{label}' eliminados correctamente que coincidían con: {match_condition}")

    # --- FIND ---
    def find(self, label, match_condition=None):
        """
        Encuentra nodos que coincidan con una condición.
        """
        condition = f"WHERE {match_condition}" if match_condition else ""
        query = f"""
        MATCH (n:{label}) {condition}
        RETURN n
        """
        with self.driver.session() as session:
            results = session.run(query)
            return [self.model.from_dict(record["n"]._properties) for record in results]

if __name__ == "__main__":
    """
from Neo4jModel import Neo4jModel
from Neo4jManager import Neo4jManager

# Definir un modelo específico heredando de Neo4jModel
class Persona(Neo4jModel):
    def __init__(self, nombre, edad, ciudad):
        super().__init__(nombre=nombre, edad=edad, ciudad=ciudad)

# Inicializar el manager con el modelo Persona
manager = Neo4jManager(model=Persona, uri="bolt://localhost:7687", user="neo4j", password="password")

# Insertar un nodo
manager.insert("Persona", {"nombre": "Elieser", "edad": 30, "ciudad": "CDMX"})

# Actualizar nodos
manager.update("Persona", "n.nombre = 'Elieser'", {"ciudad": "Guadalajara"})

# Buscar nodos
resultados = manager.find("Persona", "n.edad >= 30")
for persona in resultados:
    print(persona.to_dict())

# Eliminar nodos
manager.delete("Persona", "n.nombre = 'Elieser'")

# Cerrar conexión
manager.close()

    """