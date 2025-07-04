# vista/pantalla_login.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from controlador.usuario_controlador import login_usuario

class PantallaLogin(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout()
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        btn_ingresar = QPushButton("Ingresar")
        btn_regresar = QPushButton("Regresar")

        btn_ingresar.clicked.connect(self.iniciar_sesion)
        btn_regresar.clicked.connect(self.regresar)

        layout.addWidget(QLabel("Inicio de sesión"))
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_pass)
        layout.addWidget(btn_ingresar)
        layout.addWidget(btn_regresar)
        self.setLayout(layout)

    def iniciar_sesion(self):
        usuario = self.input_usuario.text()
        clave = self.input_pass.text()

        exito, rol = login_usuario(usuario, clave)
        if exito:
            self.input_usuario.clear()
            self.input_pass.clear()
            if rol == "Administrador":
                self.stack.setCurrentIndex(2)
            else:
                self.stack.setCurrentIndex(3)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def regresar(self):
        self.input_usuario.clear()
        self.input_pass.clear()
        self.stack.setCurrentIndex(0)
