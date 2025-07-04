# distribuidora/vista/pantalla_bienvenida.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class PantallaBienvenida(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Bienvenida")
        self.setLayout(self.crear_interfaz())
        self.showMaximized()  # 🟢 Ocupa toda la pantalla al abrir

    def crear_interfaz(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Bienvenido al sistema de la Distribuidora")
        label.setStyleSheet("font-size: 28px; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setStyleSheet("font-size: 20px; padding: 10px 20px;")
        btn_login.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addWidget(label)
        layout.addWidget(btn_login)
        return layout
