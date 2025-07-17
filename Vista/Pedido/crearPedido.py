from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QLineEdit, QCompleter, QDoubleSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from Vista.Pedido.tablaPedidos import TablaPedido

class CrearPedidos(QWidget):
    # Señales para comunicarse con el controlador
    agregar_producto_signal = pyqtSignal(str, int)  # producto, cantidad
    eliminar_fila_signal = pyqtSignal(int)  # fila
    cambiar_cantidad_signal = pyqtSignal(int, int)  # fila, nueva_cantidad
    guardar_pedido_signal = pyqtSignal(str, int, float, int)  # cliente, estado, pendiente, plazo
    resetear_pedido_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pedidos")

        self.total_actual = 0.0
        self.productos_seleccionados = []

        self.pantalla()

    def set_total_actual(self, total):
        self.total_actual = total
        self.actualizar_total(total)

    def get_total_actual(self):
        return self.total_actual

    def set_productos_seleccionados(self, productos):
        self.productos_seleccionados = productos

    def get_productos_seleccionados(self):
        return self.productos_seleccionados

    def pantalla(self):
        layout = QVBoxLayout()
        
        # Formulario de arriba
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Cliente:"))
        self.line_cliente = QLineEdit()
        self.line_cliente.setPlaceholderText("Ingrese nombre o DUI")
        form_layout.addWidget(self.line_cliente)
        
        form_layout.addWidget(QLabel("Producto:"))
        self.line_producto = QLineEdit()
        self.line_producto.setPlaceholderText("Ingrese el código o nombre del producto")
        form_layout.addWidget(self.line_producto)
        
        form_layout.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        form_layout.addWidget(self.spin_cantidad)
        
        self.btn_agregar = QPushButton("Agregar producto")
        self.btn_agregar.clicked.connect(self.agregar_producto)
        form_layout.addWidget(self.btn_agregar)
        
        layout.addLayout(form_layout)
        
        # Tabla heredada
        self.tabla = TablaPedido()
        layout.addWidget(self.tabla)
        
        self.label_total = QLabel("Total: $0.00")
        layout.addWidget(self.label_total)
        
        # Botones de tabla
        botones_layout = QHBoxLayout()
        self.btn_cambiar_cantidad = QPushButton("Cambiar cantidad")
        self.btn_cambiar_cantidad.clicked.connect(self.cambiar_cantidad)
        botones_layout.addWidget(self.btn_cambiar_cantidad)
        
        self.btn_eliminar_fila = QPushButton("Eliminar fila")
        self.btn_eliminar_fila.clicked.connect(self.eliminar_fila)
        botones_layout.addWidget(self.btn_eliminar_fila)
        
        self.btn_limpiar_pedido = QPushButton("Limpiar pedido")
        self.btn_limpiar_pedido.clicked.connect(self.resetear_pedido)
        botones_layout.addWidget(self.btn_limpiar_pedido)
        
        layout.addLayout(botones_layout)
        
        # Labels para el estado del pedido
        layout_estado = QHBoxLayout()
        self.label_estado = QLabel("Estado: ")
        self.combo_estado = QComboBox()
        self.label_pendiente_pago = QLabel("Pendiente de pagar: ")
        self.spin_pendiente = QDoubleSpinBox()
        self.spin_pendiente.setMinimum(0.00)
        self.label_plazo_dias = QLabel("Plazo de días para pagar: ")
        self.spin_plazo = QSpinBox()
        self.spin_plazo.setMinimum(0)
        
        layout_estado.addWidget(self.label_estado)
        layout_estado.addWidget(self.combo_estado)
        layout_estado.addWidget(self.label_pendiente_pago)
        layout_estado.addWidget(self.spin_pendiente)
        layout_estado.addWidget(self.label_plazo_dias)
        layout_estado.addWidget(self.spin_plazo)
        
        layout.addLayout(layout_estado)
        
        # Botones de abajo
        layout_eliminar = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar pedido")
        self.btn_guardar.clicked.connect(self.guardar_pedido)
        layout_eliminar.addWidget(self.btn_guardar)
        
        self.btn_regresar = QPushButton("Regresar a Pedidos")
        layout_eliminar.addWidget(self.btn_regresar)
        
        layout.addLayout(layout_eliminar)
        self.setLayout(layout)
    
    # Métodos para conectarse con el controlador
    def agregar_producto(self):
        texto_producto = self.line_producto.text()
        cantidad = self.spin_cantidad.value()
        self.agregar_producto_signal.emit(texto_producto, cantidad)
    
    def cargar_estados(self, lista_estados):
        self.combo_estado.clear()
        for id_estado, nombre_estado in lista_estados:
            self.combo_estado.addItem(nombre_estado, id_estado)

    def eliminar_fila(self):
        fila = self.tabla.currentRow()
        if fila != -1:
            self.eliminar_fila_signal.emit(fila)
    
    def cambiar_cantidad(self):
        fila = self.tabla.currentRow()
        if fila != -1:
            cantidad_actual = int(self.tabla.item(fila, 3).text())
            self.cambiar_cantidad_signal.emit(fila, cantidad_actual)

    def guardar_pedido(self):
        cliente = self.line_cliente.text()
        estado = self.combo_estado.currentData()
        pendiente = self.spin_pendiente.value()
        plazo = self.spin_plazo.value()
        self.guardar_pedido_signal.emit(cliente, estado, pendiente, plazo)
    
    def resetear_pedido(self):
        self.resetear_pedido_signal.emit()
    
    # Actualizar la vista 
    def autocompletado_productos(self, lista_productos):
        completer = QCompleter(lista_productos)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.line_producto.setCompleter(completer)
    
    def autocompletado_clientes(self, lista_clientes):
        completer = QCompleter(lista_clientes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.line_cliente.setCompleter(completer)
    
    def agregar_fila_tabla(self, id_producto, descripcion, precio, cantidad, subtotal):
        self.tabla.agregar_fila(id_producto, descripcion, precio, cantidad, subtotal)
    
    def actualizar_total(self, total):
        self.label_total.setText(f"Total: ${total:.2f}")
    
    def eliminar_fila_tabla(self, fila):
        self.tabla.removeRow(fila)
    
    def actualizar_cantidad_fila(self, fila, nueva_cantidad, nuevo_subtotal):
        self.tabla.setItem(fila, 3, QTableWidgetItem(str(nueva_cantidad)))
        self.tabla.setItem(fila, 4, QTableWidgetItem(f"${nuevo_subtotal:.2f}"))
    
    def limpiar(self):
        self.tabla.limpiar()
        self.label_total.setText("Total: $0.00")
        self.combo_estado.setCurrentIndex(0)
        self.line_cliente.clear()
        self.line_producto.clear()
        self.spin_cantidad.setValue(1)
        self.spin_plazo.setValue(0)
        self.spin_pendiente.setValue(0)
        self.total_actual = 0.0
        self.productos_seleccionados = []
    
    def fila_seleccionada(self):
        return self.tabla.currentRow()
    
    def obtener_cantidad_fila(self, fila):
        return int(self.tabla.item(fila, 3).text())
    
    def obtener_descripcion_fila(self, fila):
        return self.tabla.item(fila, 1).text()
