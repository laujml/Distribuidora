# Consolidado/stock_bajo_modelo.py

from Modelo.db_config import conectar

class StockBajoModelo:
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()

    def obtener_productos_stock_bajo(self, limite=7):
        self.cursor.execute("""
            SELECT descripcion, stockActual 
            FROM Productos 
            WHERE stockActual BETWEEN 0 AND %s
        """, (limite,))
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()
