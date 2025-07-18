from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtCore import Qt
from Vista.Usuario.pantalla_bienvenida import PantallaBienvenida
from Vista.Usuario.pantalla_login import PantallaLogin
from Recursos.Styles import Styles
from MenuGestionPedidos import MenuGestionPedidos

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Distribuidora")
        self.resize(900, 600)

        # Pantallas
        self.pantalla_bienvenida = PantallaBienvenida(self)
        self.pantalla_login = PantallaLogin(self)
        self.menu_gestion = MenuGestionPedidos(self)  # Agrega MenuGestionPedidos al stack

        # Agregar al stack
        self.addWidget(self.pantalla_bienvenida)  # index 0
        self.addWidget(self.pantalla_login)       # index 1
        self.addWidget(self.menu_gestion)         # index 2

        self.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(Styles.global_stylesheet())
    ventana = MainApp()
    ventana.setWindowTitle("Sistema Distribuidora")
    ventana.resize(500, 500)
    ventana.show()
    app.exec()

