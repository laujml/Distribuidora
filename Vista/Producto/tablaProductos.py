from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class TablaProductosView(QWidget):
    """Vista para mostrar la tabla de productos"""
    
    def __init__(self, stacked_widget, controlador):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controlador = controlador
        self.resize(600, 400)
        self.configurar_interfaz()
    
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
        
        # Leyenda de colores
        leyenda_layout = QHBoxLayout()
        leyenda_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        leyenda_rojo = QLabel("🔴 Stock: 0")
        leyenda_amarillo = QLabel("🟡 Stock: 1-7")
        
        leyenda_layout.addWidget(leyenda_rojo)
        leyenda_layout.addWidget(leyenda_amarillo)
        
        layout.addLayout(leyenda_layout)
        
        # Botones pequeños y centrados en una fila
        botones_layout = QHBoxLayout()
        botones_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.setFixedWidth(160)
        btn_actualizar.clicked.connect(self.actualizar_tabla)
        botones_layout.addWidget(btn_actualizar)
        
        btn_importar = QPushButton("Importar desde Excel")
        btn_importar.setFixedWidth(160)
        btn_importar.clicked.connect(self.importar_excel)
        botones_layout.addWidget(btn_importar)
        
        layout.addLayout(botones_layout)
        
        # Botón regresar (centrado debajo)
        btn_regresar = QPushButton("<- Regresar")
        btn_regresar.setFixedWidth(160)
        btn_regresar.clicked.connect(self.volver_menu)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
    
    def actualizar_tabla(self, productos=None):
        """Actualiza la tabla con los productos y aplica colores según stock"""
        if isinstance(productos, bool) or productos is None:
            self.controlador.cargar_tabla_productos()
        else:
            self._llenar_tabla_con_colores(productos)
    
    def _llenar_tabla_con_colores(self, productos):
        """Llena la tabla aplicando colores según el stock"""
        self.tabla.setRowCount(len(productos))
        
        for row_idx, producto in enumerate(productos):
            # Obtener el stock (columna índice 5)
            stock = 0
            try:
                stock = int(producto[5]) if producto[5] is not None else 0
            except (ValueError, IndexError):
                stock = 0
            
            # Determinar el color de fondo según el stock
            color_fondo = self.obtener_color_stock(stock)
            
            # Llenar las celdas de la fila
            for col_idx, dato in enumerate(producto):
                item = QTableWidgetItem(str(dato))
                
                # Aplicar color de fondo siempre
                if color_fondo:
                    item.setBackground(color_fondo)
                
                # Si es la columna de stock, resaltar el texto
                if col_idx == 5:  # Columna de stock
                    if stock == 0:
                        item.setForeground(QColor(139, 0, 0))  # Texto rojo oscuro
                    elif stock <= 7:
                        item.setForeground(QColor(184, 134, 11))  # Texto amarillo oscuro
                
                self.tabla.setItem(row_idx, col_idx, item)

    def obtener_color_stock(self, stock):
        """Retorna el color de fondo basado en el stock"""
        if stock == 0:
            return QColor(255, 204, 204)  # Rojo claro
        elif stock <= 7:
            return QColor(255, 255, 204)  # Amarillo claro
        else:
            return None  # Sin color (blanco por defecto)
    
    def importar_excel(self):
        """Maneja la importación desde Excel"""
        self.controlador.importar_desde_excel()
    
    def volver_menu(self):
        """Vuelve al menú principal"""
        self.controlador.volver_menu_principal()
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", mensaje)
    
    def mostrar_exito(self, mensaje):
        """Muestra un mensaje de éxito"""
        QMessageBox.information(self, "Éxito", mensaje)
