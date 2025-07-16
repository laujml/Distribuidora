from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class TablaPedido(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)  # Inicializa con 0 filas y 5 columnas
        self.setHorizontalHeaderLabels(["Codigo", "Producto", "Precio", "Cantidad", "Subtotal"])

    def limpiar(self):
        self.setRowCount(0)

    def agregar_fila(self, codigo, producto, precio, cantidad, subtotal):
        fila = self.rowCount()
        self.insertRow(fila)
        self.setItem(fila, 0, QTableWidgetItem(str(codigo)))
        self.setItem(fila, 1, QTableWidgetItem(str(producto)))
        self.setItem(fila, 2, QTableWidgetItem(f"${precio:.2f}"))
        self.setItem(fila, 3, QTableWidgetItem(str(cantidad)))
        self.setItem(fila, 4, QTableWidgetItem(f"${subtotal:.2f}"))

    def obtener_datos(self):
        datos = []
        for fila in range(self.rowCount()):
            codigo = self.item(fila, 0).text()
            producto = self.item(fila, 1).text()
            precio = self.item(fila, 2).text().replace("$", "")
            cantidad = self.item(fila, 3).text()
            subtotal = self.item(fila, 4).text().replace("$", "")
            datos.append((codigo, producto, float(precio), int(cantidad), float(subtotal)))
        return datos
