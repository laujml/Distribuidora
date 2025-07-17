from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize
import os

class PantallaBienvenida(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = QLabel(self)
        logo_path = os.path.join(os.path.dirname(__file__), "../recursos/logo.jpg")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            rounded_pixmap = self.redondear_pixmap(pixmap, 240)
            logo_label.setPixmap(rounded_pixmap)
        else:
            logo_label.setText("LOGO")
            logo_label.setStyleSheet("border: 2px solid white; border-radius: 120px; width: 240px; height: 240px;")
        
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Título
        label = QLabel("¡Bienvenido!", self)
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")
        
        # Botón
        boton = QPushButton("Iniciar sesión", self)
        boton.setFixedSize(250, 35)
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
