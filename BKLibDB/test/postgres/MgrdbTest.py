from BKLibDB.BKManager.BKManagerDB import BKManagerDB
from ModelTest import Test

class MgrdbTest(BKManagerDB):
    """
    Manager para manejar operaciones CRUD en la tabla public.test.
    """
    def __init__(self, **kwargs):
        """
        Inicializa el manager con la configuración de la base de datos.
        """
        super().__init__(model=Test, **kwargs)

    def get_sql_select(self):
        return """
            SELECT id, nombre, valor
            FROM public.test
        """

    def get_sql_insert(self):
        return """
            INSERT INTO public.test (id, nombre, valor)
            VALUES (:id, :nombre, :valor)
        """

    def get_sql_update(self):
        return """
            UPDATE public.test
            SET nombre = :nombre,
                valor = :valor
            WHERE id = :id
        """

    def get_sql_delete(self):
        return """
            DELETE FROM public.test
            WHERE id = :id
        """

    # Métodos personalizados
    def select_all(self):
        """
        Retorna todos los registros de la tabla.
        """
        sql = "SELECT id, nombre, valor FROM public.test ORDER BY id"
        return self.fetch_all(sql)
