from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QIcon
from Consolidado import ventanaPedido 
from Recursos.Styles import Styles 
from Consolidado.ventanaClientes import MainClientes
from Consolidado.ventanaProveedores import MainProveedores
from Vista.Dashboard.pantalla_dashboard import PantallaDashboard
from Consolidado.ventanaPedido import VentanaPedidos

class MenuGestionPedidos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Pedidos de Distribuidora Josue")
        
        # Diccionario para cachear widgets y evitar recrearlos constantemente
        self.widgets_cache = {}
        
        # Variable para trackear el índice actual
        self.current_index = -1
        
        self.menu()
    
    def menu(self):
        layout_principal = QHBoxLayout(self)
        
        # Menú lateral (layout vertical con logo y lista)
        layout_menu_lateral = QVBoxLayout()
        layout_principal.addLayout(layout_menu_lateral, 1)
        
        # Lista del menú
        self.lista_menu = QListWidget()
        self.lista_menu.setObjectName("menuLateral")
        self.lista_menu.currentRowChanged.connect(self.entrar_ventana_seguro)
        layout_menu_lateral.addWidget(self.lista_menu)
        
        logo_item = QListWidgetItem()
        logo_icon = QIcon("Recursos/logo.jpg")
        logo_item.setIcon(logo_icon)
        logo_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.lista_menu.setIconSize(QSize(100, 100))
        self.lista_menu.addItem(logo_item)
        
        # Ítems del menú
        opciones = [
            "DashBoard",
            "Clientes", 
            "Pedidos",        
            "Productos",
            "Proveedores",
            "Reportes",
            "Cerrar Sesión"
        ]
        
        for opcion in opciones:
            self.lista_menu.addItem(QListWidgetItem(opcion))
        
        # Panel derecho 
        self.stacked_widget = QStackedWidget()
        layout_principal.addWidget(self.stacked_widget, 3)
        
        # Precargar VentanaPedidos
        try:
            ventana_pedidos = ventanaPedido.VentanaPedidos()
            self.widgets_cache[3] = ventana_pedidos
            self.stacked_widget.addWidget(ventana_pedidos)
        except Exception as e:
            error_widget = QLabel(f"Error al precargar Pedidos: {str(e)}")
            error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets_cache[3] = error_widget
            self.stacked_widget.addWidget(error_widget)
    
    def entrar_ventana_seguro(self, index):
        if index == self.current_index:
            return
        QTimer.singleShot(50, lambda: self.entrar_ventana(index))
    
    def entrar_ventana(self, index):
        self.current_index = index
        
        if index in self.widgets_cache:
            widget = self.widgets_cache[index]
            self.stacked_widget.setCurrentWidget(widget)
            return
        
        widget = None
        
        if index == 1:  # DashBoard
            widget = QLabel("Bienvenido al Dashboard")
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        elif index == 2:  # Clientes
            widget = MainClientes()
            
        elif index == 4:  # Productos
            widget = QLabel("Ventana de Productos")
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        elif index == 5:  # Proveedores
            widget = MainProveedores()
            
        elif index == 6:  # Reportes
            widget = QLabel("Ventana de Reportes")
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        elif index == 7:  # Cerrar sesión
            self.close()
            return
        
        if widget:
            self.widgets_cache[index] = widget
            self.stacked_widget.addWidget(widget)
            self.stacked_widget.setCurrentWidget(widget)

    def limpiar_cache(self):
        for index, widget in self.widgets_cache.items():
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.widgets_cache.clear()
    
    def closeEvent(self, event):
        self.limpiar_cache()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    
    window = MenuGestionPedidos()
    Styles.aplicar_estilo_global(window, window.lista_menu)
    
    window.resize(800, 600)
    window.show()
    
    app.exec()
