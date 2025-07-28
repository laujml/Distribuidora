# Uso de PyQt6, os(para lectura) y sys
# La pantalla de bienvenida es la primera pantalla a mostrarse al correr la aplicacion. Su fin es meramente estetico para poder trasladarse al login.
# Ventana no indispensable y no afecta al resto del codigo
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QApplication
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize
import os
import sys
from Recursos.Styles import Styles

class PantallaBienvenida(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Carga de Logo
        logo_label = QLabel(self)
        logo_label.setObjectName("logoLabel")
        logo_path = "Recursos/logo.jpg"
        
        # Ajuste de tamaño
        # En caso de que el logo no cargue o no exista se proyecta la palabra "LOGO"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            rounded_pixmap = self.redondear_pixmap(pixmap, 240)
            logo_label.setPixmap(rounded_pixmap)
        else:
            logo_label.setText("LOGO")
            logo_label.setObjectName("logoLabel_fallback")
            
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Título de bienvenida
        label = QLabel("¡Bienvenido!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("titulo")

        # Botón de iniciar sesion conectado al login
        boton = QPushButton("Iniciar sesión", self)
        boton.setObjectName("btn_bienvenida")
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

    # Cambio de index a 1(Pantalla de login)
    def ir_a_login(self):
        self.stack.setCurrentIndex(1)
