from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
)
from PyQt6.QtGui import QPixmap, QFont, QPainter, QPainterPath
import os
from PyQt6.QtCore import Qt
from controlador.login_controlador import LoginControlador

class PantallaLogin(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setup_ui()
        self.controlador = LoginControlador(self, stack)
        
        self.btn_ingresar.clicked.connect(self.controlador.ingresar)
        self.btn_regresar.clicked.connect(self.controlador.regresar)
        
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

        self.logo = QLabel()
        self.logo.setFixedSize(100, 100)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = os.path.join(os.path.dirname(__file__), "../componentes/logo.jpg")
        pixmap = QPixmap(logo_path)
        rounded_pixmap = self.redondear_pixmap(pixmap, 100)
        self.logo.setPixmap(rounded_pixmap)

        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_container.addWidget(self.logo)
        layout_form.addLayout(logo_container)

        
        self.lbl_titulo = QLabel("Inicio de sesion")
        self.lbl_titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.lbl_titulo.setStyleSheet("color: white;")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_form.addWidget(self.lbl_titulo)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Usuario")
        self.txt_usuario.setFixedHeight(40)
        self.txt_usuario.setStyleSheet("""
            border-radius: 20px;
            background-color: #A9A9A9;
            padding-left: 15px;
            font-size: 14px;
        """)
        layout_form.addWidget(self.txt_usuario)

        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Contraseña")
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_contrasena.setFixedHeight(40)
        self.txt_contrasena.setStyleSheet("""
            border-radius: 20px;
            background-color: #A9A9A9;
            padding-left: 15px;
            font-size: 14px;
        """)
        layout_form.addWidget(self.txt_contrasena)

                
        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.setFixedHeight(30)
        self.btn_ingresar.setStyleSheet("""
            background-color: white;
            color: black;
            border-radius: 5px;
            font-weight: bold;
        """)
        layout_form.addWidget(self.btn_ingresar)


        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFixedHeight(30)
        self.btn_regresar.setStyleSheet("""
            background-color: white;
            color: black;
            border-radius: 5px;
            font-weight: bold;
        """)
        layout_form.addWidget(self.btn_regresar)

        
        layout_horizontal.addWidget(contenedor)
        layout_general.addLayout(layout_horizontal)

        
        layout_general.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        
        self.btn_ingresar.setEnabled(True)
        self.btn_ingresar.setVisible(True)
        self.btn_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ingresar.raise_()

        self.btn_regresar.setEnabled(True)
        self.btn_regresar.setVisible(True)
        self.btn_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_regresar.raise_()

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

