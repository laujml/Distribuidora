# Consolidado/stock_bajo_controlador.py

from Modelo.stockBajo_modelo import StockBajoModelo

class StockBajoControlador:
    def __init__(self, limite=7):
        self.limite = limite

    def verificar_stock_bajo(self):
        modelo = StockBajoModelo()
        productos = modelo.obtener_productos_stock_bajo(self.limite)
        modelo.cerrar_conexion()
        return productos
