from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from Modelo.ui_config import UIConfig

class PantallaSeleccion(QWidget):
    ir_a_semanal_signal = pyqtSignal()
    ir_a_mensual_signal = pyqtSignal()

    def __init__(self, stack, controller):
        super().__init__()
        self.stack = stack
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        UIConfig.configure_layout(layout)

        titulo = QLabel("Seleccione Tipo de Reporte")
        UIConfig.configure_label(titulo, is_title=True)
        layout.addWidget(titulo)

        btn_semanal = QPushButton("Reporte Semanal")
        UIConfig.configure_control(btn_semanal)
        btn_semanal.clicked.connect(self.show_semanal_report)
        layout.addWidget(btn_semanal)

        btn_mensual = QPushButton("Reporte Mensual")
        UIConfig.configure_control(btn_mensual)
        btn_mensual.clicked.connect(self.show_mensual_report)
        layout.addWidget(btn_mensual)

        layout.addStretch()
        self.setLayout(layout)

    def show_semanal_report(self):
        self.ir_a_semanal_signal.emit()
        self.controller.mostrar_reporte("Semanal")
        self.stack.setCurrentIndex(1)

    def show_mensual_report(self):
        self.ir_a_mensual_signal.emit()
        self.controller.mostrar_reporte("Mensual")
        self.stack.setCurrentIndex(1)
