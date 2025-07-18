from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class PantallaSeleccion(QWidget):
    ir_a_semanal = pyqtSignal()  
    ir_a_mensual = pyqtSignal()  

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titulo = QLabel("Seleccione Tipo de Reporte")
        self.content_layout.addWidget(self.titulo)

        self.btn_semanal = QPushButton("Reporte Semanal")
        self.btn_semanal.clicked.connect(self.go_to_weekly)
        self.btn_semanal.setFixedSize(400, 100)
        self.content_layout.addWidget(self.btn_semanal)

        self.btn_mensual = QPushButton("Reporte Mensual")

        self.btn_mensual.clicked.connect(self.go_to_monthly)
        self.btn_mensual.setFixedSize(400, 100)
        self.content_layout.addWidget(self.btn_mensual)

        self.content_layout.addStretch()
        self.setLayout(self.content_layout)

    def go_to_weekly(self):
        self.ir_a_semanal.emit()
        self.stack.setCurrentIndex(1)

    def go_to_monthly(self):
        self.ir_a_mensual.emit()
        self.stack.setCurrentIndex(1)
