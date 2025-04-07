from BKLibDB.BKModel.BKModel_Base import BKColumn, BKModel

class Test(BKModel):
    """
    Modelo para la tabla public.test en PostgreSQL.
    """
    id = BKColumn("id", int, primary_key=True, doc="ID único del registro")
    nombre = BKColumn("nombre", str, doc="Nombre del elemento")
    valor = BKColumn("valor", float, doc="Valor numérico")