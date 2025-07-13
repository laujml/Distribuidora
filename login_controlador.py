from modelo.usuario_modelo import validar_credenciales
from PyQt6.QtWidgets import QMessageBox
from vista.pantalla_dashboard import PantallaDashboard
from vista.pantalla_administrador import PantallaAdministrador

class LoginControlador:
    def __init__(self, vista_login, stack):
        self.vista = vista_login
        self.stack = stack
        self.dashboard_index = None
        self.admin_index = None  

    def ingresar(self):
        # Corrección: Indentación correcta del método
        usuario = self.vista.txt_usuario.text()
        contrasena = self.vista.txt_contrasena.text()

        login_ok, datos_usuario = validar_credenciales(usuario, contrasena)

        if login_ok:
            rol = datos_usuario["tipoUsuario"].lower()

            if rol == "administrador":
                if self.admin_index is None:
                    admin = PantallaAdministrador(self.stack)  # Usando PantallaAdministrador
                    self.admin_index = self.stack.addWidget(admin)
                self.stack.setCurrentIndex(self.admin_index)

            elif rol == "cliente":
                if self.dashboard_index is None:
                    dashboard = PantallaDashboard(self.stack, usuario=datos_usuario["nombreUsuario"])
                    self.dashboard_index = self.stack.addWidget(dashboard)
                self.stack.setCurrentIndex(self.dashboard_index)
            else:
                QMessageBox.warning(self.vista, "Error", f"Rol desconocido: {rol}")
        else:
            QMessageBox.warning(self.vista, "Error", "Credenciales inválidas")

    def mostrar_error(self, mensaje):
        QMessageBox.warning(self.vista, "Error", mensaje)

    def regresar(self):
        self.stack.setCurrentIndex(0)