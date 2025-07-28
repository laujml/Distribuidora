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

# Importar los componentes de reportes
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Vista.Reporte.vista_reportes import ReportesView
from Controlador.Reporte.controlador_reportes import ReportesController

#IMportar productos
from Consolidado.main_productos import crear_sistema_productos


class MenuGestionPedidos(QWidget):
    def __init__(self, stack): 
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Pedidos de Distribuidora Josue")
        self.stack = stack

        # Diccionario para cachear widgets y evitar recrearlos constantemente
        self.widgets_cache = {}

        # Variable para trackear el índice actual
        self.current_index = -1

        # Stack para reportes (será creado cuando se necesite)
        self.reportes_stack = None
        self.reportes_controller = None

        self.menu()

    def menu(self):
        layout_principal = QHBoxLayout(self)

        # ✅ Contenedor con ancho fijo para el menú lateral
        menu_container = QWidget()
        menu_container.setFixedWidth(140)  # Ancho fijo de 250px
        menu_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        # Layout del menú lateral
        layout_menu_lateral = QVBoxLayout(menu_container)
        layout_menu_lateral.setContentsMargins(0, 0, 0, 0)  # Sin márgenes adicionales

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

        # ✅ Agregar el contenedor del menú al layout principal
        layout_principal.addWidget(menu_container)

        # Panel derecho con el contenido principal
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout_principal.addWidget(self.stacked_widget)  # Sin factor de stretch, toma todo el espacio restante

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

    def crear_sistema_reportes(self):
        """Crea el sistema de reportes completo"""
        try:
            # Crear el stack para reportes
            self.reportes_stack = QStackedWidget()
            
            # Crear la vista de reportes
            reportes_view = ReportesView()
            
            # Crear la pantalla de selección
            seleccion = PantallaSeleccion(self.reportes_stack, None)  # Temporalmente sin controlador
            
            # Agregar las vistas al stack de reportes
            self.reportes_stack.addWidget(seleccion)      # Índice 0
            self.reportes_stack.addWidget(reportes_view)  # Índice 1
            
            # AHORA crear el controlador con el stack ya poblado
            self.reportes_controller = ReportesController(reportes_view, self.reportes_stack)
            
            # Asignar el controlador a la pantalla de selección
            seleccion.controller = self.reportes_controller
            
            # Conectar las señales manualmente para asegurar que funcionen
            seleccion.ir_a_semanal_signal.connect(lambda: self.reportes_controller.mostrar_reporte("Semanal"))
            seleccion.ir_a_mensual_signal.connect(lambda: self.reportes_controller.mostrar_reporte("Mensual"))
            
            # Establecer la pantalla inicial (selección)
            self.reportes_stack.setCurrentIndex(0)
            
            return self.reportes_stack
            
        except Exception as e:
            error_widget = QLabel(f"Error al crear sistema de reportes: {str(e)}")
            error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_widget.setStyleSheet("""
                QLabel {
                    color: red;
                    font-size: 14px;
                    padding: 20px;
                }
            """)
            return error_widget

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
                widget_productos = crear_sistema_productos()
                self.widgets_cache[index] = widget_productos  
                self.stacked_widget.addWidget(widget_productos)
                self.stacked_widget.setCurrentWidget(widget_productos)
            except Exception as e:
                error_widget = QLabel(f"Error al cargar Productos: {str(e)}")

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
                # Crear el sistema de reportes si no existe
                if self.reportes_stack is None:
                    widget_reportes = self.crear_sistema_reportes()
                    self.widgets_cache[index] = widget_reportes
                    self.stacked_widget.addWidget(widget_reportes)
                    self.stacked_widget.setCurrentWidget(widget_reportes)
                else:
                    # Si ya existe, solo mostrarlo
                    widget_reportes = self.widgets_cache[index]
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
        # Cerrar el controlador de reportes si existe
        if self.reportes_controller:
            try:
                self.reportes_controller.close()
            except:
                pass
            
        for index, widget in self.widgets_cache.items():
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.widgets_cache.clear()
        
        # Limpiar referencias
        self.reportes_stack = None
        self.reportes_controller = None

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
