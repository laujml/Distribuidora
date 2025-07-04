# vista/dialogo_modificar_usuario.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from controlador.usuario_controlador import cambiar_contrasena

class ModificarUsuarioDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar usuario")

        layout = QVBoxLayout()
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario existente")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Nueva contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_modificar = QPushButton("Modificar")
        btn_modificar.clicked.connect(self.modificar_usuario)

        layout.addWidget(self.usuario)
        layout.addWidget(self.password)
        layout.addWidget(btn_modificar)
        self.setLayout(layout)

    def modificar_usuario(self):
        nombre = self.usuario.text()
        clave = self.password.text()

        if cambiar_contrasena(nombre, clave):
            QMessageBox.information(self, "Éxito", "Contraseña modificada.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario no existe.")
