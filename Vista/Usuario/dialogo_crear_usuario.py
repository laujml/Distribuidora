# Se hace uso de PyQt6 y Controlador.usuario
#Dialogo para crear usuario es una ventana emergente que requiere de los datos "rol", "usuario" y "contraseña".
# Se ejecuta unicamente al entrar por medio de la pantalla del administrador haciendo click en "Crear nuevo usuario"
#Los datos quedan almacenados en la Base de Datos de la distribuidora
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from Controlador.Usuario.usuario_controlador import registrar_nuevo_usuario

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

        #Conexion del boton guardar con guardar_usuario
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_usuario)

        layout.addWidget(QLabel("Rol"))
        layout.addWidget(self.combo_rol)
        layout.addWidget(self.usuario)
        layout.addWidget(self.password)
        layout.addWidget(btn_guardar)
        self.setLayout(layout)

    #Se pide la informacion de usuario, password y el rol de usuario o administrador. Si no se llenan todos los campos se muestra una advertencia y no se guardan
    # hasta que los campos sean completados. Se muestra confirmacion de guardado
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
