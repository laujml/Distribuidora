from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget, QListWidgetItem,
    QMessageBox, QTableWidgetItem
)
from Vista.crearPedido import CrearPedidos
from Modelo.modelo import Modelo

class EditarPedido(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Pedido")
        self.modelo = Modelo()
        self.pedidos = self.modelo.obtener_datos_pedido()
        self.pedido_actual = None

        self.editarPedido()

    def editarPedido(self):
        layout_principal = QHBoxLayout(self)

        # Lista de pedidos a la izquierda
        self.lista_pedidos = QListWidget()
        self.lista_pedidos.currentRowChanged.connect(self.cargar_pedido_en_formulario)
        layout_principal.addWidget(self.lista_pedidos, 1)

        # Formulario editable (heredado de CrearPedidos)
        self.formulario = CrearPedidos()
        self.formulario.btn_guardar.setText("Guardar Cambios")
        self.formulario.btn_guardar.clicked.disconnect()
        self.formulario.btn_guardar.clicked.connect(self.guardar_cambios)

        layout_principal.addWidget(self.formulario, 3)

        self.cargar_lista_pedidos()

    def cargar_lista_pedidos(self):
        self.lista_pedidos.clear()
        for pedido in self.pedidos:
            item = QListWidgetItem(f"Pedido #{pedido['numero']}")
            self.lista_pedidos.addItem(item)
        if self.pedidos:
            self.lista_pedidos.setCurrentRow(0)

    def cargar_pedido_en_formulario(self, index):
        if index < 0 or index >= len(self.pedidos):
            return

        pedido = self.pedidos[index]
        self.pedido_actual = pedido

        self.formulario.resetear_pedido()
        self.formulario.line_cliente.setText(f"{pedido['cliente_id']} - {pedido['nombre']}")
        self.formulario.line_estado.setText(pedido['estado'])
        self.formulario.spin_pendiente.setValue(pedido['pendiente_pagar'])
        self.formulario.spin_plazo.setValue(pedido['plazo_dias'])

        self.formulario.productos_seleccionados.clear()
        self.formulario.tabla.setRowCount(0)
        total = 0

        for producto in pedido["productos"]:
            id_producto = producto["codigo"]
            nombre = producto["nombre"]
            precio = producto["precio"]
            cantidad = producto["cantidad"]
            subtotal = producto["subtotal"]
            total += subtotal

            fila = self.formulario.tabla.rowCount()
            self.formulario.tabla.insertRow(fila)
            self.formulario.tabla.setItem(fila, 0, QTableWidgetItem(nombre))
            self.formulario.tabla.setItem(fila, 1, QTableWidgetItem(f"${precio:.2f}"))
            self.formulario.tabla.setItem(fila, 2, QTableWidgetItem(str(cantidad)))
            self.formulario.tabla.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))

            self.formulario.productos_seleccionados.append([id_producto, cantidad, subtotal])

        self.formulario.total = total
        self.formulario.label_total.setText(f"Total: ${total:.2f}")

    def guardar_cambios(self):
        if not self.pedido_actual:
            return

        try:
            texto_cliente = self.formulario.line_cliente.text()
            id_cliente = texto_cliente.split("-")[0].strip()
            estado = self.formulario.line_estado.text()
            pendiente = self.formulario.spin_pendiente.value()
            plazo = self.formulario.spin_plazo.value()
            total = self.formulario.total
            detalles = self.formulario.productos_seleccionados
            id_pedido = self.pedido_actual["numero"]

            exito = self.modelo.actualizar_pedido(id_pedido, id_cliente, total, estado, pendiente, plazo, detalles)
            if exito:
                QMessageBox.information(self, "Éxito", f"Pedido #{id_pedido} actualizado correctamente.")
                self.pedidos = self.modelo.obtener_datos_pedido()
                self.cargar_lista_pedidos()
            else:
                QMessageBox.critical(self, "Error", "Ocurrió un error al actualizar el pedido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cambios: {e}")
