from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QStackedWidget, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QIcon

#Componentes de pedidos:
from Consolidado.ventanaPedido import VentanaPedidos
from Consolidado.ventanaClientes import MainClientes

#componente de proveedores
from Consolidado.ventanaProveedores import MainProveedores

#componente del dashboard
from Vista.Dashboard.pantalla_dashboard import PantallaDashboard

#Importar productos
from Consolidado.ventanaProducto import AplicacionProductos

# Importar la función de reportes
from Consolidado.ventanaReportes import crear_modulo_reportes  # O el archivo donde pongas la función

class MenuGestionPedidos(QWidget):
    def __init__(self, stack): 
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Pedidos de Distribuidora Josue")
        self.stack = stack

        # Diccionario para cachear widgets y evitar recrearlos constantemente
        self.widgets_cache = {}

        # Variable para trackear el índice actual
        self.current_index = -1

        self.menu()

    def menu(self):
        layout_principal = QHBoxLayout(self)

        # Contenedor con ancho fijo para el menú lateral
        menu_container = QWidget()
        menu_container.setFixedWidth(150)
        menu_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        # Layout del menú lateral
        layout_menu_lateral = QVBoxLayout(menu_container)
        layout_menu_lateral.setContentsMargins(0, 0, 0, 0)

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

        # Agregar el contenedor del menú al layout principal
        layout_principal.addWidget(menu_container)

        # Panel derecho con el contenido principal
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout_principal.addWidget(self.stacked_widget) 

        # Precargar Dashboard (índice 1)
        try:
            ventana_dashboard = PantallaDashboard(stack=None)
            self.widgets_cache[1] = ventana_dashboard
            self.stacked_widget.addWidget(ventana_dashboard)
        except Exception as e:
            error_widget = QLabel(f"Error al precargar Dashboard: {str(e)}")
            error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets_cache[1] = error_widget
            self.stacked_widget.addWidget(error_widget)

        # Precargar Pedidos (índice 3)
        try:
            ventana_pedidos = VentanaPedidos()
            self.widgets_cache[3] = ventana_pedidos
            self.stacked_widget.addWidget(ventana_pedidos)
        except Exception as e:
            error_widget = QLabel(f"Error al precargar Pedidos: {str(e)}")
            error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widgets_cache[3] = error_widget
            self.stacked_widget.addWidget(error_widget)

    def entrar_ventana_seguro(self, index):
        """Evita conflictos al cambiar entre ventanas"""
        if index == self.current_index:
            return
        QTimer.singleShot(50, lambda: self.entrar_ventana(index))

    def entrar_ventana(self, index):
        """Maneja el cambio de ventana con caché de widgets"""
        self.current_index = index

        if index in self.widgets_cache:
            widget = self.widgets_cache[index]
            self.stacked_widget.setCurrentWidget(widget)
            return

        widget = None

        if index == 2:  # Clientes
            try:
                widget_clientes = MainClientes()
                self.widgets_cache[index] = widget_clientes  
                self.stacked_widget.addWidget(widget_clientes)
                self.stacked_widget.setCurrentWidget(widget_clientes)
            except Exception as e:
                error_widget = QLabel(f"Error al cargar Clientes: {str(e)}")
                error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets_cache[index] = error_widget
                self.stacked_widget.addWidget(error_widget)
                self.stacked_widget.setCurrentWidget(error_widget)

        elif index == 4:  # Productos
            try:
                widget_productos = AplicacionProductos(parent=self)  # Pasar parent
                widget_productos_main = widget_productos.stacked_widget
                self.widgets_cache[index] = widget_productos_main
                self.stacked_widget.addWidget(widget_productos_main)
                self.stacked_widget.setCurrentWidget(widget_productos_main)
            except Exception as e:
                error_widget = QLabel(f"Error al cargar Productos: {str(e)}")
                error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets_cache[index] = error_widget
                self.stacked_widget.addWidget(error_widget)
                self.stacked_widget.setCurrentWidget(error_widget)

        elif index == 5:  # Proveedores
            try:
                widget_proveedores = MainProveedores()
                self.widgets_cache[index] = widget_proveedores  # Guardar en caché
                self.stacked_widget.addWidget(widget_proveedores)
                self.stacked_widget.setCurrentWidget(widget_proveedores)  # Mostrar en pantalla
            except Exception as e:
                error_widget = QLabel(f"Error al cargar Proveedores: {str(e)}")
                error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets_cache[index] = error_widget
                self.stacked_widget.addWidget(error_widget)
                self.stacked_widget.setCurrentWidget(error_widget)
        
        elif index == 6:  # Reportes
            try:
                # Crear módulo de reportes usando la función reutilizable
                widget_reportes = crear_modulo_reportes()
                self.widgets_cache[index] = widget_reportes
                self.stacked_widget.addWidget(widget_reportes)
                self.stacked_widget.setCurrentWidget(widget_reportes)
            except Exception as e:
                error_widget = QLabel(f"Error al cargar Reportes: {str(e)}")
                error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.widgets_cache[index] = error_widget
                self.stacked_widget.addWidget(error_widget)
                self.stacked_widget.setCurrentWidget(error_widget)
            return

        elif index == 7:  # Cerrar sesión
            confirm = QMessageBox.question(self, "Cerrar sesión", "¿Desea cerrar sesión?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.stack.setCurrentIndex(0)  # Volver a la pantalla de bienvenida
            return

        if widget:
            self.widgets_cache[index] = widget
            self.stacked_widget.addWidget(widget)
            self.stacked_widget.setCurrentWidget(widget)

    def limpiar_cache(self):
        """Limpia el caché de widgets si es necesario"""
        for index, widget in self.widgets_cache.items():
            if widget:
                # Si es el widget de reportes, cerrar conexiones DB
                if index == 6 and hasattr(widget, 'reportes_controller'):
                    try:
                        widget.reportes_controller.close()
                    except:
                        pass
                        
                widget.setParent(None)
                widget.deleteLater()
        self.widgets_cache.clear()

    def closeEvent(self, event):
        """Limpia recursos al cerrar"""
        self.limpiar_cache()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = MenuGestionPedidos(usuario="Administrador")
    #app.setStyleSheet(Styles.global_stylesheet())
    window.show()
    app.exec()
