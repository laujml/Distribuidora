# Vista/TablaProductosView.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt

class TablaProductosView(QWidget):
    """Vista para mostrar la tabla de productos"""
    
    def __init__(self, stacked_widget, controlador):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controlador = controlador  # Referencia al controlador
        self.resize(600, 400)
        self.configurar_interfaz()
        # Cargar datos iniciales
    
    def configurar_interfaz(self):
        """Configura la interfaz de la tabla"""
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Lista de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)
        
        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Descripción", "Precio", "Talla", "Color",
            "Stock", "Fecha ingreso", "ID Proveedor"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        self.crear_botones(layout)
        
        self.setLayout(layout)
    
    def crear_botones(self, layout):
        """Crea los botones de la vista"""
        # Botón actualizar
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.actualizar_tabla)
        layout.addWidget(btn_actualizar)
        
        # Botón importar desde Excel
        btn_importar = QPushButton("Importar desde Excel")
        btn_importar.clicked.connect(self.importar_excel)
        layout.addWidget(btn_importar)
        
        # Botón regresar
        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_menu)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def actualizar_tabla(self, productos=None):
        if isinstance(productos, bool) or productos is None:
            self.controlador.cargar_tabla_productos()
        else:
            self.tabla.setRowCount(len(productos))
            for row_idx, producto in enumerate(productos):
                for col_idx, dato in enumerate(producto):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(dato)))

    def importar_excel(self):
        """Maneja la importación desde Excel - Delega al controlador"""
        self.controlador.importar_desde_excel()
    
    def volver_menu(self):
        """Vuelve al menú principal - Delega al controlador"""
        self.controlador.volver_menu_principal()
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", mensaje)
    
    def mostrar_exito(self, mensaje):
        """Muestra un mensaje de éxito"""
        QMessageBox.information(self, "Éxito", mensaje)
