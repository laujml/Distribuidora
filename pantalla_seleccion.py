from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from recursos.Styles import Styles

class PantallaSeleccion(QWidget):
    ir_a_semanal = pyqtSignal()
    ir_a_mensual = pyqtSignal()

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Seleccione Tipo de Reporte")
        Styles.apply_styles(titulo)
        layout.addWidget(titulo)

        btn_semanal = QPushButton("Reporte Semanal")
        Styles.apply_styles(btn_semanal)
        btn_semanal.clicked.connect(self.ir_a_semanal)
        layout.addWidget(btn_semanal)

        btn_mensual = QPushButton("Reporte Mensual")
        Styles.apply_styles(btn_mensual)
        btn_mensual.clicked.connect(self.ir_a_mensual)
        layout.addWidget(btn_mensual)

        layout.addStretch()
        self.setLayout(layout)