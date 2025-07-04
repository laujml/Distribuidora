# main.py
import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from vista.pantalla_bienvenida import PantallaBienvenida
from vista.pantalla_login import PantallaLogin
from vista.pantalla_administrador import PantallaAdministrador
from vista.pantalla_dashboard import PantallaDashboard

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    stack.addWidget(PantallaBienvenida(stack))     # I 0
    stack.addWidget(PantallaLogin(stack))          # I 1
    stack.addWidget(PantallaAdministrador(stack))  # I 2
    stack.addWidget(PantallaDashboard())           # I 3

    stack.showMaximized()
    stack.setWindowTitle("Gestión de Pedidos")
    stack.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
