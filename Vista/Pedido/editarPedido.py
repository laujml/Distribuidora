from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget, QListWidgetItem,
    QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal
from Vista.Pedido.crearPedido import CrearPedidos

class EditarPedido(CrearPedidos):
    pedido_seleccionado = pyqtSignal(int)  # Índice del pedido seleccionado
    guardar_cambios = pyqtSignal()         # Solicitud de guardar cambios

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Pedido")
        self.pantallas()
        self.conectar_señales()

    def pantallas(self):
        # Crear layout principal: lista de pedidos a la izquierda, formulario a la derecha
        layout_principal = QHBoxLayout()

        # Lista de pedidos
        self.lista_pedidos = QListWidget()
        self.lista_pedidos.setObjectName("panelIzquierdo")
        layout_principal.addWidget(self.lista_pedidos, 1)

        # Obtener layout actual del formulario heredado (CrearPedidos)
        formulario_layout = self.layout()
        contenedor_formulario = QWidget()
        contenedor_formulario.setLayout(formulario_layout)

        layout_principal.addWidget(contenedor_formulario, 3)

        # Establecer layout final en el widget heredado
        self.setLayout(layout_principal)

    def conectar_señales(self):
        self.lista_pedidos.currentRowChanged.connect(self.intermedio_pedido_seleccionado)
        self.btn_guardar.clicked.disconnect()
        self.btn_guardar.setText("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios.emit)

    def intermedio_pedido_seleccionado(self, index):
        self.pedido_seleccionado.emit(index)

    def cargar_lista_pedidos(self, pedidos):
        self.lista_pedidos.clear()
        for pedido in pedidos:
            item = QListWidgetItem(f"Pedido #{pedido['numero']}")
            self.lista_pedidos.addItem(item)
        if pedidos:
            self.lista_pedidos.setCurrentRow(0)

    def cargar_pedido_en_formulario(self, pedido):
        self.resetear_pedido()

        self.line_cliente.setText(f"{pedido['cliente_id']} - {pedido['nombre']}")
        for i in range(self.combo_estado.count()):
            if self.combo_estado.itemData(i) == pedido["estado_id"]:
                self.combo_estado.setCurrentIndex(i)
                break
        self.spin_pendiente.setValue(pedido['pendiente_pagar'])
        self.spin_plazo.setValue(pedido['plazo_dias'])

        self.productos_seleccionados.clear()
        self.tabla.setRowCount(0)
        total = 0

        for producto in pedido["productos"]:
            id_producto = producto["codigo"]
            nombre = producto["nombre"]
            precio = producto["precio"]
            cantidad = producto["cantidad"]
            subtotal = producto["subtotal"]
            total += subtotal

            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(id_producto)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila, 2, QTableWidgetItem(f"${precio:.2f}"))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(fila, 4, QTableWidgetItem(f"${subtotal:.2f}"))

            self.productos_seleccionados.append([id_producto, cantidad, subtotal])

        self.total_actual = total
        self.label_total.setText(f"Total: ${total:.2f}")

    def obtener_datos_formulario(self):
        detalles = []
        for fila in range(self.tabla.rowCount()):
            id_producto = self.tabla.item(fila, 0).text()
            cantidad = int(self.tabla.item(fila, 3).text())
            subtotal = float(self.tabla.item(fila, 4).text().replace("$", "").strip())
            detalles.append([id_producto, cantidad, subtotal])

        return {
            'texto_cliente': self.line_cliente.text(),
            'estado': self.combo_estado.currentData(),
            'pendiente': self.spin_pendiente.value(),
            'plazo': self.spin_plazo.value(),
            'total': sum([item[2] for item in detalles]),
            'detalles': detalles
        }

    def actualizar_lista_pedidos(self, pedidos):
        indice_actual = self.lista_pedidos.currentRow()
        self.cargar_lista_pedidos(pedidos)
        if 0 <= indice_actual < len(pedidos):
            self.lista_pedidos.setCurrentRow(indice_actual)

    def get_productos_seleccionados(self):
        return self.productos_seleccionados
