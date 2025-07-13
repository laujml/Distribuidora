from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class MenuLateral(QWidget):
    def __init__(self, stack=None, usuario=None, opciones=None):
        super().__init__()
        self.stack = stack
        self.usuario = usuario
        self.botones = {}

        self.setObjectName("menuLateral")
        self.setFixedWidth(200)

        self.setStyleSheet("""
            QWidget#menuLateral {
                background-color: white;
            }

            QLabel#logoLabel {
                margin-top: 20px;
                margin-bottom: 20px;
            }

            QPushButton {
                border: none;
                background-color: white;
                font-size: 15px;
                color: #3f4c53;
                font-weight: bold;
                padding: 15px 0px;
            }

            QPushButton:hover {
                background-color: #f0f0f0;
            }

            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        lbl_logo = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "logo.jpg"))
        lbl_logo.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_logo)

        # Botones de navegación
        self.opciones = opciones or []
        for texto in self.opciones:
            btn = QPushButton(texto)
            btn.clicked.connect(lambda checked, t=texto: self.on_opcion_seleccionada(t))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
            self.botones[texto] = btn

        self.opcion_cambiada_callback = None

    def on_opcion_seleccionada(self, texto):
        print(f">>> Opción seleccionada: {texto}")

        # Aqui irian las demas pestañas del menu lateral. EJEMPLO
        """
        if texto == "Clientes":
            self.stack.setCurrentIndex(1)
        elif texto == "Pedidos":
            self.stack.setCurrentIndex(2)
        ...
        """

        if self.opcion_cambiada_callback:
            self.opcion_cambiada_callback(texto)

    def set_callback_opcion_cambiada(self, callback):
        self.opcion_cambiada_callback = callback
