from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, 
    QHBoxLayout, QLabel, QComboBox, QSpinBox,QPushButton,
    QTableWidgetItem, QMessageBox, QInputDialog, QDoubleSpinBox, 
    QLineEdit, QCompleter)

from PyQt6.QtCore import Qt
from Modelo.modelo import Modelo

class CrearPedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pedidos")
        self.modelo = Modelo()
        self.total = 0.0
        self.productos_disponibles = {}  
        self.productos_seleccionados = []
        self.clientela = {}  

        self.TablaPedido()
        self.cargar_productos()
        self.cargar_clientes() #se declaran estas variable en el init para que cuando se 
        #cree una instacia de "CrearPedidos", se incialicen las funciones de una sola vez y esten listas para ser usadas

    def TablaPedido(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Cliente:"))
        self.line_cliente = QLineEdit()
        self.line_cliente.setPlaceholderText("Ingrese nombre o DUI")
        form_layout.addWidget(self.line_cliente)

        form_layout.addWidget(QLabel("Producto:"))
        self.combo_producto = QComboBox()
        form_layout.addWidget(self.combo_producto)
        
        form_layout.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        form_layout.addWidget(self.spin_cantidad)

        self.btn_agregar = QPushButton("Agregar producto")
        self.btn_agregar.clicked.connect(self.agregar_producto)
        form_layout.addWidget(self.btn_agregar)

        layout.addLayout(form_layout)

        # Tabla 
        self.tabla = QTableWidget(0, 4) #"Crea una tabla vacia, sin filas todavia, pero con 4 columnas ya definidas. Son como dimensiones de la tabla inciales".
        self.tabla.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Subtotal"])
        layout.addWidget(self.tabla)

        # Total
        self.label_total = QLabel("Total: $0.00")
        layout.addWidget(self.label_total)

        #Botones para eliminar filas y cambiar la cantidad de producto
        botones_layout = QHBoxLayout()

        self.btn_cambiar_cantidad = QPushButton("Cambiar cantidad")
        self.btn_cambiar_cantidad.clicked.connect(self.cambiar_cantidad_fila)
        botones_layout.addWidget(self.btn_cambiar_cantidad)

        self.btn_eliminar_fila = QPushButton("Eliminar fila")
        self.btn_eliminar_fila.clicked.connect(self.eliminar_fila)
        botones_layout.addWidget(self.btn_eliminar_fila)

        # Guardar
        self.btn_limpiar_pedido = QPushButton("Limpiar pedido")
        self.btn_limpiar_pedido.clicked.connect(self.resetear_pedido)
        botones_layout.addWidget(self.btn_limpiar_pedido)
        layout.addLayout(botones_layout)

        #Botones de estado del pedido
        layout_estado = QHBoxLayout()
        self.label_estado = QLabel("Estado: ")
        self.line_estado = QLineEdit()

        self.label_pendiente_Pago = QLabel("Pendiente de pagar: ")
        self.spin_pendiente = QDoubleSpinBox()
        self.spin_pendiente.setMinimum(00.00)

        self.label_plazo_dias = QLabel("Plaza de dias para pagar: ")
        self.spin_plazo = QSpinBox()
        self.spin_plazo.setMinimum(0)

        layout_estado.addWidget(self.label_estado)
        layout_estado.addWidget(self.line_estado)
        layout_estado.addWidget(self.label_pendiente_Pago)
        layout_estado.addWidget(self.spin_pendiente)
        layout_estado.addWidget(self.label_plazo_dias)
        layout_estado.addWidget(self.spin_plazo)
        layout.addLayout(layout_estado)

        layout_eliminar = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar pedido")
        self.btn_guardar.clicked.connect(self.guardar_pedido)
        layout_eliminar.addWidget(self.btn_guardar)

        self.btn_regresar = QPushButton("Regresar a Pedidos")
        layout_eliminar.addWidget(self.btn_regresar)

        layout.addLayout(layout_eliminar)

        self.setLayout(layout)

    def cargar_productos(self):
        productos = self.modelo.obtener_productos()
        
        self.combo_producto.clear() #clear sirve para limpiar datos antiguos y no tener duplicados
        self.productos_disponibles.clear()

        for id_producto, descripcion, precio in productos:
            self.combo_producto.addItem(descripcion)
            self.productos_disponibles[descripcion] = (id_producto, precio)    

    def cargar_clientes(self):
        clientes = self.modelo.obtener_clientes()
        self.line_cliente.clear()

        completer = QCompleter(clientes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains) #Autocompletar
        self.line_cliente.setCompleter(completer)

    def agregar_producto(self):        
        nombre = self.combo_producto.currentText()
        cantidad = self.spin_cantidad.value()

        if nombre not in self.productos_disponibles:
            return

        id_producto, precio = self.productos_disponibles[nombre]
        subtotal = float(precio * cantidad)

        fila = self.tabla.rowCount() #indica el índice en el que se insertará una nueva fila.
        self.tabla.insertRow(fila) #Inserta una nueva fila en la posición fila
        self.tabla.setItem(fila, 0, QTableWidgetItem(nombre)) #columna en la posicion 0
        self.tabla.setItem(fila, 1, QTableWidgetItem(f"${precio:.2f}"))
        self.tabla.setItem(fila, 2, QTableWidgetItem(str(cantidad)))
        self.tabla.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))
        
        self.productos_seleccionados.append([id_producto, cantidad, subtotal])
        self.actualizar_total()

        #cada vez que se preciona el boton agregar producto se ejecuta esta funcion, por ello, se agregan nuevas filas "dinamicamente"

    def guardar_pedido(self):
        try:
            if not self.productos_seleccionados:
                QMessageBox.warning(self, "Advertencia", "No hay productos en el pedido.")
                return

            texto_cliente = self.line_cliente.text()
            id_cliente = texto_cliente.split("-")[0] if "-" in texto_cliente else None #El [0] sirve para obtener la parte antes del guion en el texto
            estado = self.line_estado.text()
            pendiente_pagar = self.spin_pendiente.value()
            plazo_dias = self.spin_plazo.value()

            id_pedido = self.modelo.crear_pedido(id_cliente, self.total, estado, pendiente_pagar, plazo_dias)
            self.modelo.agregar_detalle_y_actualizar_stock(id_pedido, self.productos_seleccionados)

            QMessageBox.information(self, "Éxito", f"Pedido #{id_pedido} guardado correctamente.")
            self.resetear_pedido()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el pedido:\n{e}")

    def actualizar_total(self):
        self.total = sum(float(item[2]) for item in self.productos_seleccionados)
        self.label_total.setText(f"Total: ${self.total:.2f}")

    def eliminar_fila(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione una fila para eliminar.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Está seguro de eliminar la fila seleccionada?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            self.tabla.removeRow(fila)
            self.productos_seleccionados.pop(fila)
            self.actualizar_total()

    def cambiar_cantidad_fila(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione una fila para cambiar la cantidad.")
            return

        cantidad_actual = int(self.tabla.item(fila, 2).text())
        nuevo_valor, ok = QInputDialog.getInt(self, "Cambiar cantidad",
                                             "Ingrese nueva cantidad:",
                                             value=cantidad_actual, min=1)
        if ok:
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(nuevo_valor)))

            # Recalcular subtotal
            nombre = self.tabla.item(fila, 0).text()
            id_producto, precio = self.productos_disponibles[nombre]
            nuevo_subtotal = precio * nuevo_valor
            self.tabla.setItem(fila, 3, QTableWidgetItem(f"${nuevo_subtotal:.2f}"))

            # Actualizar lista productos seleccionados
            self.productos_seleccionados[fila][1] = nuevo_valor
            self.productos_seleccionados[fila][2] = nuevo_subtotal

            self.actualizar_total()          

    def resetear_pedido(self):
        self.tabla.setRowCount(0)
        self.label_total.setText("Total: $0.00")
        self.total = 0.0
        self.productos_seleccionados.clear()
        self.line_estado.setText("")
        self.line_cliente.setText("")
        self.spin_plazo.setValue(0)
        self.spin_pendiente.setValue(0)
