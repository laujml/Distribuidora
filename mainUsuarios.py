# MAIN
import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from vista.pantalla_bienvenida import PantallaBienvenida
from vista.pantalla_login import PantallaLogin
from vista.pantalla_administrador import PantallaAdministrador
from controlador.login_controlador import LoginControlador
from vista.pantalla_dashboard import PantallaDashboard

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #4d5a62; }")

    stack = QStackedWidget()

    # Creacion de pantallas
    bienvenida = PantallaBienvenida(stack)
    login = PantallaLogin(stack)
    dashboard = PantallaDashboard(stack,usuario="Cliente") 
    admin = PantallaAdministrador(stack)

    #Controlador del login
    login_controlador = LoginControlador(login, stack)

    # Agregar pantallas al stack
    stack.addWidget(bienvenida)   # Índice 0
    stack.addWidget(login)        # Índice 1
    stack.addWidget(dashboard)    # Índice 2
    stack.addWidget(admin)        # Índice 3

    #Pantalla de bienvenida al inicio
    stack.setCurrentIndex(0)
    stack.setWindowTitle("Gestión de Pedidos")
    stack.showMaximized()
    stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
