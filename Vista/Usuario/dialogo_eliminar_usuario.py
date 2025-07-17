# vista/dialogo_eliminar_usuario.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from Controlador.Usuario.usuario_controlador import eliminar_usuario_existente

class EliminarUsuarioDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eliminar usuario")

        layout = QVBoxLayout()
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario a eliminar")

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_usuario)

        layout.addWidget(self.usuario)
        layout.addWidget(btn_eliminar)
        self.setLayout(layout)

    def eliminar_usuario(self):
        nombre = self.usuario.text()

        if eliminar_usuario_existente(nombre):
            QMessageBox.information(self, "Éxito", "Usuario eliminado.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario no existe.")
