#Uso de PyQt6, os, sys y Controlador.Usuario
# Es la primera pantalla que ejerce un funcionamiento de la aplicacion. Se trata de la parte visual y conexion para poder validar los datos del login
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
)
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath
from PyQt6.QtCore import Qt
from Controlador.Usuario.login_controlador import LoginControlador
import os
import sys

class PantallaLogin(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.controlador = LoginControlador(self, stack)
        self.setup_ui()
        
        # Conectar eventos
        self.btn_ingresar.clicked.connect(self.controlador.ingresar)
        self.btn_regresar.clicked.connect(self.controlador.regresar)
        
        # Permitir login con Enter
        self.txt_contrasena.returnPressed.connect(self.controlador.ingresar)
    
    def setup_ui(self):
        layout_general = QVBoxLayout(self)
        layout_general.setContentsMargins(0, 0, 0, 0)
        layout_general.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        contenedor = QFrame()
        contenedor.setFixedWidth(350)
        layout_form = QVBoxLayout(contenedor)
        layout_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_form.setSpacing(20)
        
        # Logo
        self.logo = QLabel()
        self.logo.setFixedSize(100, 100)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_path = "Recursos/logo.jpg"
        pixmap = QPixmap(logo_path)
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            rounded_pixmap = self.redondear_pixmap(pixmap, 100)
            self.logo.setPixmap(rounded_pixmap)
        else:
            self.logo.setText("LOGO")
            self.logo.setStyleSheet("border: 2px solid white; border-radius: 50px;")
        
        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_container.addWidget(self.logo)
        layout_form.addLayout(logo_container)
        
        # Título
        self.lbl_titulo = QLabel("Inicio de sesión")
        self.lbl_titulo.setObjectName("titulo")
        layout_form.addWidget(self.lbl_titulo)
        
        # Campos de entrada
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Usuario")
        self.txt_usuario.setFixedHeight(40)
        layout_form.addWidget(self.txt_usuario)
        
        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Contraseña")
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_contrasena.setFixedHeight(40)
        layout_form.addWidget(self.txt_contrasena)
        
        # Botones
        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.setFixedHeight(30)
        self.btn_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)
        layout_form.addWidget(self.btn_ingresar)
        
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFixedHeight(30)
        self.btn_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        layout_form.addWidget(self.btn_regresar)
        
        layout_horizontal.addWidget(contenedor)
        layout_general.addLayout(layout_horizontal)
        layout_general.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    
    def redondear_pixmap(self, pixmap, diameter):
        pixmap = pixmap.scaled(diameter, diameter, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        rounded = QPixmap(diameter, diameter)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, diameter, diameter)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded
