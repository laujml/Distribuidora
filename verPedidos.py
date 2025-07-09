from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QPushButton, QListWidget, 
    QListWidgetItem, QMessageBox)

from Modelo.modelo import Modelo  

class VerPedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pedidos")
        self.modelo = Modelo()
        self.pedidos = self.modelo.obtener_datos_pedido()
        self.pedido_actual = None
        self.design()
        self.cargarPedidos()

    def design(self):
        layout_principal = QHBoxLayout(self)

        # Lista de pedidos a la izquierda
        self.lista_pedidos = QListWidget()
        self.lista_pedidos.currentRowChanged.connect(self.mostrar_detalle_pedido)
        layout_principal.addWidget(self.lista_pedidos, 1)

        # Widget detalle pedido a la derecha
        self.detalle_widget = QWidget()
        detalle_layout = QVBoxLayout(self.detalle_widget)

        # Labels con info del pedido
        layout_label = QHBoxLayout()
        self.label_fecha = QLabel("Fecha: ")
        self.label_numero = QLabel("No. de pedido: ")
        self.label_cliente_id = QLabel("Ident. del cliente: ")
        self.label_nombre = QLabel("Nombre: ")

        layout_label.addWidget(self.label_fecha)
        layout_label.addWidget(self.label_numero)
        layout_label.addWidget(self.label_cliente_id)
        layout_label.addWidget(self.label_nombre)
        
        detalle_layout.addLayout(layout_label) 

        # Tabla con productos
        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(["Codigo", "Producto", "Precio", "Cantidad", "Subtotal"])
        detalle_layout.addWidget(self.tabla)

        # Total y estado
        self.label_total = QLabel("Total: $0.00")
        self.label_estado = QLabel("Estado: ")
        self.label_pendiente_pagar = QLabel("Monto pendiente: $")
        self.label_plazo_dias = QLabel("Plazo de días para pagar: ")

        detalle_layout.addWidget(self.label_total)
        detalle_layout.addWidget(self.label_estado)
        detalle_layout.addWidget(self.label_pendiente_pagar)
        detalle_layout.addWidget(self.label_plazo_dias)

        # Botones
        self.btn_eliminar = QPushButton("Cancelar (Eliminar) pedido")
        self.btn_eliminar.clicked.connect(self.eliminarPedido)
        detalle_layout.addWidget(self.btn_eliminar)

        layout_principal.addWidget(self.detalle_widget, 3) #revisar

    def cargarPedidos(self):
        self.lista_pedidos.clear()
        for pedido in self.pedidos:
            item = QListWidgetItem(f"Pedido #{pedido['numero']}")
            self.lista_pedidos.addItem(item)

        if self.pedidos:
            self.lista_pedidos.setCurrentRow(0)
        else:
            self.limpiarDetalle()

    def mostrar_detalle_pedido(self, indice):
        if indice < 0 or indice >= len(self.pedidos):
            self.limpiarDetalle()
            return

        pedido = self.pedidos[indice]
        self.pedido_actual = pedido

        self.label_fecha.setText(f"Fecha: {pedido['fecha']}")
        self.label_numero.setText(f"No. de pedido: {pedido['numero']}")
        self.label_cliente_id.setText(f"Ident. del cliente: {pedido['cliente_id']}")
        self.label_nombre.setText(f"Nombre: {pedido['nombre']}")

        # Llenar tabla productos
        self.tabla.setRowCount(0)
        for producto in pedido["productos"]:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(producto["codigo"])))
            self.tabla.setItem(row, 1, QTableWidgetItem(producto["nombre"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(f"${producto['precio']:.2f}"))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(producto["cantidad"])))
            self.tabla.setItem(row, 4, QTableWidgetItem(f"${producto['subtotal']:.2f}"))

        self.label_total.setText(f"Total: ${pedido['total']:.2f}")
        self.label_estado.setText(f"Estado: {pedido['estado']}")
        self.label_pendiente_pagar.setText(f"Monto pendiente: ${pedido['pendiente_pagar']:.2f}")
        self.label_plazo_dias.setText(f"Plazo de días para pagar: {pedido['plazo_dias']}")

    def limpiarDetalle(self):
        self.pedido_actual = None
        self.label_fecha.setText("Fecha: ")
        self.label_numero.setText("No. de pedido: ")
        self.label_cliente_id.setText("Ident. del cliente: ")
        self.label_nombre.setText("Nombre: ")
        self.tabla.setRowCount(0)
        self.label_total.setText("Total: $0.00")
        self.label_estado.setText("Estado: ")
        self.label_pendiente_pagar.setText("Monto pendiente: $")
        self.label_plazo_dias.setText("Plazo de días para pagar: ")

    def eliminarPedido(self):
        if not self.pedido_actual:
            return

        pedido = self.pedido_actual
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Seguro que quieres eliminar el pedido #{pedido['numero']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.modelo.eliminar_pedido(pedido["numero"])
            QMessageBox.information(self, "Éxito", "Pedido eliminado correctamente.")

            # Actualizar lista y refrescar vista
            self.pedidos = [p for p in self.pedidos if p["numero"] != pedido["numero"]]
            self.cargarPedidos()
            