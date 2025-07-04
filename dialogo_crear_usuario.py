# vista/dialogo_crear_usuario.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from controlador.usuario_controlador import registrar_nuevo_usuario

class CrearUsuarioDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear nuevo usuario")

        layout = QVBoxLayout()
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["Administrador", "Cliente"])
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_usuario)

        layout.addWidget(QLabel("Rol"))
        layout.addWidget(self.combo_rol)
        layout.addWidget(self.usuario)
        layout.addWidget(self.password)
        layout.addWidget(btn_guardar)
        self.setLayout(layout)

    def guardar_usuario(self):
        nombre = self.usuario.text()
        clave = self.password.text()
        rol = self.combo_rol.currentText()

        if not nombre or not clave:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        if registrar_nuevo_usuario(nombre, clave, rol):
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario ya existe.")
