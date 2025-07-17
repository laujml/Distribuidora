from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from vista.tablaPedidos import TablaPedido

class VerPedidos(QWidget):
    # Señales para comunicarse con el controlador
    pedido_seleccionado = pyqtSignal(int)
    eliminar_pedido_solicitado = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pedidos")
        self.pantalla()
        
    def pantalla(self):
        layout_principal = QHBoxLayout(self)
        
        # Lista de pedidos
        self.lista_pedidos = QListWidget()
        self.lista_pedidos.setObjectName("panelIzquierdo")
        self.lista_pedidos.currentRowChanged.connect(self.pedido_seleccionado.emit)
        layout_principal.addWidget(self.lista_pedidos, 1)
        
        # Detalle del pedido
        self.detalle_widget = QWidget()
        detalle_layout = QVBoxLayout(self.detalle_widget)
        
        # Información general
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
        
        # Tabla de productos del padre (Reutilizada)
        self.tabla = TablaPedido()
        detalle_layout.addWidget(self.tabla)
        
        # Totales y estado
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
        self.btn_eliminar.clicked.connect(self.eliminar_pedido_solicitado.emit)
        self.btn_regresar = QPushButton("Regresar a Pedidos")
        detalle_layout.addWidget(self.btn_eliminar)
        detalle_layout.addWidget(self.btn_regresar)
        
        layout_principal.addWidget(self.detalle_widget, 3)
    
    def mostrar_lista_pedidos(self, pedidos):
        """Actualiza la lista de pedidos en la interfaz"""
        self.lista_pedidos.clear()
        for pedido in pedidos:
            item = QListWidgetItem(f"Pedido #{pedido['numero']}")
            self.lista_pedidos.addItem(item)
        
        if pedidos:
            self.lista_pedidos.setCurrentRow(0)
        else:
            self.limpiar_detalle()
    
    def mostrar_detalle_pedido(self, pedido):
        """Actualiza el detalle del pedido en la interfaz"""
        self.label_fecha.setText(f"Fecha: {pedido['fecha']}")
        self.label_numero.setText(f"No. de pedido: {pedido['numero']}")
        self.label_cliente_id.setText(f"Ident. del cliente: {pedido['cliente_id']}")
        self.label_nombre.setText(f"Nombre: {pedido['nombre']}")
        
        # Poblar tabla
        self.tabla.limpiar()
        for producto in pedido["productos"]:
            self.tabla.agregar_fila(
                producto["codigo"],
                producto["nombre"],
                producto["precio"],
                producto["cantidad"],
                producto["subtotal"]
            )
        
        self.label_total.setText(f"Total: ${pedido['total']:.2f}")
        self.label_estado.setText(f"Estado: {pedido['estado']}")
        self.label_pendiente_pagar.setText(f"Monto pendiente: ${pedido['pendiente_pagar']:.2f}")
        self.label_plazo_dias.setText(f"Plazo de días para pagar: {pedido['plazo_dias']}")
    
    def limpiar_detalle(self):
        """Limpia el detalle del pedido"""
        self.label_fecha.setText("Fecha: ")
        self.label_numero.setText("No. de pedido: ")
        self.label_cliente_id.setText("Ident. del cliente: ")
        self.label_nombre.setText("Nombre: ")
        self.tabla.limpiar()
        self.label_total.setText("Total: $0.00")
        self.label_estado.setText("Estado: ")
        self.label_pendiente_pagar.setText("Monto pendiente: $")
        self.label_plazo_dias.setText("Plazo de días para pagar: ")
    
    def mostrar_confirmacion_eliminacion(self, numero_pedido):
        """Muestra diálogo de confirmación para eliminar pedido"""
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Seguro que quieres eliminar el pedido #{numero_pedido}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return respuesta == QMessageBox.StandardButton.Yes
    
    def mostrar_mensaje_exito(self, mensaje):
        """Muestra mensaje de éxito"""
        QMessageBox.information(self, "Éxito", mensaje)
    
    def mostrar_mensaje_error(self, mensaje):
        """Muestra mensaje de error"""
        QMessageBox.critical(self, "Error", mensaje)
    
    def obtener_indice_seleccionado(self):
        """Obtiene el índice del pedido seleccionado"""
        return self.lista_pedidos.currentRow()
