from Modelo.usuario_modelo import validar_credenciales
from PyQt6.QtWidgets import QMessageBox
from Vista.Usuario.pantalla_administrador import PantallaAdministrador

class LoginControlador:
    def __init__(self, vista_login, stack):
        self.vista = vista_login
        self.stack = stack

    def ingresar(self):
        usuario = self.vista.txt_usuario.text()
        contrasena = self.vista.txt_contrasena.text()

        login_ok, datos_usuario = validar_credenciales(usuario, contrasena)

        if login_ok:
            rol = datos_usuario["tipoUsuario"].lower()

            if rol == "administrador":
                admin = PantallaAdministrador(self.stack)
                admin_index = self.stack.addWidget(admin)
                self.stack.setCurrentIndex(admin_index)

            elif rol == "cliente":
                self.stack.setCurrentIndex(2)  # Cambia al menú ya cargado

            else:
                QMessageBox.warning(self.vista, "Error", f"Rol desconocido: {rol}")
        else:
            QMessageBox.warning(self.vista, "Error", "Credenciales inválidas")

    def regresar(self):
        self.stack.setCurrentIndex(0)

