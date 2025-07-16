from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize
from recursos.Styles import Styles


class PantallaBienvenida(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #4d5a62;")



        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    
        logo_label = QLabel(self)
        pixmap = QPixmap("distribuidora/componentes/logo.jpg").scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        rounded_pixmap = self.redondear_pixmap(pixmap, 240)
        logo_label.setPixmap(rounded_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        
        label = QLabel("¡Bienvenido!", self)
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")

        
        boton = QPushButton("Iniciar sesión", self)
        boton.setFixedSize(250, 35)
        boton.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        boton.clicked.connect(self.ir_a_login)

        layout.addWidget(logo_label)
        layout.addSpacing(20)
        layout.addWidget(label)
        layout.addSpacing(15)
        layout.addWidget(boton)

        self.setLayout(layout)

    def redondear_pixmap(self, pixmap, diameter):
        rounded = QPixmap(QSize(diameter, diameter))
        rounded.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, diameter, diameter)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded

    def ir_a_login(self):
        self.stack.setCurrentIndex(1)
