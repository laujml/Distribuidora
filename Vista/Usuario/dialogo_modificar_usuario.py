# Se hace uso de PyQt6 y Controlador.usuario
#Dialogo para Modificar usuario es una ventana emergente que requiere del dato "usuario".
# Se ejecuta unicamente al entrar por medio de la pantalla del administrador haciendo click en "Modificar usuario"
#Los datos son modificados en la Base de Datos de la distribuidora
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from Controlador.Usuario.usuario_controlador import cambiar_contrasena

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
    #Si se modifica la password se muestra un mensaje de confirmacion. Si el usuario no existe se muestra una advertencia de error y la nula existencia del usuario
    def modificar_usuario(self):
        nombre = self.usuario.text()
        clave = self.password.text()

        if cambiar_contrasena(nombre, clave):
            QMessageBox.information(self, "Éxito", "Contraseña modificada.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "El usuario no existe.")
