from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Usuario.pantalla_bienvenida import PantallaBienvenida
from Vista.Usuario.pantalla_login import PantallaLogin
from Recursos.Styles import Styles

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Inicializar pantallas principales
        self.pantalla_bienvenida = PantallaBienvenida(self)
        self.pantalla_login = PantallaLogin(self)

        self.addWidget(self.pantalla_bienvenida)  # índice 0
        self.addWidget(self.pantalla_login)       # índice 1

        self.setCurrentIndex(0)

        # Se acceden desde LoginControlador (se crearán ahí)
        self.menu_gestion_index = None
        self.dashboard_index = None
        self.admin_index = None

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(Styles.global_stylesheet())
    ventana = MainApp()
    ventana.setWindowTitle("Sistema Distribuidora")
    ventana.resize(900, 600)
    ventana.show()

    sys.exit(app.exec())
