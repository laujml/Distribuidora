from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from Styles import Styles
from recursos.MenuLateral import MenuLateral

class PantallaSeleccion(QWidget):
    ir_a_semanal = pyqtSignal()  # Signal for weekly report
    ir_a_mensual = pyqtSignal()  # Signal for monthly report

    def __init__(self, stack):
        """
        Initialize the selection screen with a lateral menu.

        Args:
            stack (QStackedWidget): The stacked widget for navigation.
        """
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        """
        Set up the user interface with a lateral menu and report selection buttons.
        """
        main_layout = QHBoxLayout()

        # Lateral menu with full height
        opciones = ["Reportes", "Clientes", "Pedidos", "Productos"]
        self.menu_lateral = MenuLateral(stack=self.stack, opciones=opciones)
        self.menu_lateral.set_callback_opcion_cambiada(self.on_menu_opcion_seleccionada)
        main_layout.addWidget(self.menu_lateral, stretch=1)  # Stretch to fill left side

        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titulo = QLabel("Seleccione Tipo de Reporte")
        Styles.apply_styles(self.titulo)
        self.content_layout.addWidget(self.titulo)
        self.titulo.hide()

        self.btn_semanal = QPushButton("Reporte Semanal")
        Styles.apply_styles(self.btn_semanal)
        self.btn_semanal.clicked.connect(self.go_to_weekly)
        self.btn_semanal.setFixedSize(400, 100)  # Larger button size
        self.content_layout.addWidget(self.btn_semanal)
        self.btn_semanal.hide()

        self.btn_mensual = QPushButton("Reporte Mensual")
        Styles.apply_styles(self.btn_mensual)
        self.btn_mensual.clicked.connect(self.go_to_monthly)
        self.btn_mensual.setFixedSize(400, 100)  # Larger button size
        self.content_layout.addWidget(self.btn_mensual)
        self.btn_mensual.hide()

        self.content_layout.addStretch()
        main_layout.addWidget(self.content_widget, stretch=3)  # More space for content

        self.setLayout(main_layout)

    def on_menu_opcion_seleccionada(self, opcion):
        """
        Handle menu option selection.

        Args:
            opcion (str): The selected menu option.
        """
        if opcion == "Reportes":
            self.titulo.show()
            self.btn_semanal.show()
            self.btn_mensual.show()
        else:
            self.titulo.hide()
            self.btn_semanal.hide()
            self.btn_mensual.hide()
            print(f"Navigating to {opcion} screen (implement navigation logic)")

    def go_to_weekly(self):
        """
        Emit the signal to show the weekly report and navigate to the reports view.
        """
        self.ir_a_semanal.emit()
        self.stack.setCurrentIndex(1)  # Navigate to ReportesView

    def go_to_monthly(self):
        """
        Emit the signal to show the monthly report and navigate to the reports view.
        """
        self.ir_a_mensual.emit()
        self.stack.setCurrentIndex(1)  # Navigate to ReportesView
