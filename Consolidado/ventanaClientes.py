from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStackedWidget, QToolButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import sys
from Vista.Cliente.agregar_clientes import AgregarClientes
from Vista.Cliente.buscar_clientes import BuscarClientes
from Vista.Cliente.actualizar_clientes import ActualizarClientes
from Vista.Cliente.eliminar_clientes import EliminarClientes
from Controlador.Cliente.cliente_controller import ClienteController

class MenuPrincipal(QWidget):
    def __init__(self, cambiar_vista):
        super().__init__()
        self.cambiar_vista = cambiar_vista
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Clientes")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        btn_agregar = QPushButton()
        btn_agregar.setText("Agregar cliente")
        btn_agregar.setIcon(QIcon("recursos/Agregar cliente.jpg"))
        btn_agregar.clicked.connect(lambda: self.cambiar_vista('agregar'))
        main_layout.addWidget(btn_agregar)

        btn_actualizar = QPushButton()
        btn_actualizar.setText("Actualizar cliente")
        btn_actualizar.setIcon(QIcon("recursos/Actualizar datos.jpg"))
        btn_actualizar.clicked.connect(lambda: self.cambiar_vista('actualizar'))
        main_layout.addWidget(btn_actualizar)

        btn_eliminar = QPushButton()
        btn_eliminar.setText("Eliminar cliente")
        btn_eliminar.setIcon(QIcon("recursos/Eliminar cliente.jpg"))
        btn_eliminar.clicked.connect(lambda: self.cambiar_vista('eliminar'))
        main_layout.addWidget(btn_eliminar)

        btn_buscar = QPushButton()
        btn_buscar.setText("Buscar cliente")
        btn_buscar.setIcon(QIcon("recursos/Buscar.jpg"))
        btn_buscar.clicked.connect(lambda: self.cambiar_vista('buscar'))
        main_layout.addWidget(btn_buscar)

        self.setLayout(main_layout)

class MainClientes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clientes")
        self.stacked = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self.controller = ClienteController()  # Instancia única del controlador
        self.init_vistas()

    def init_vistas(self):
        self.menu = MenuPrincipal(self.cambiar_vista)
        self.stacked.addWidget(self.menu)
        # Instancias de las ventanas de acción, pasando el controlador y el callback
        self.ventanas = {
            'agregar': AgregarClientes(self.controller, lambda: self.cambiar_vista('menu')),
            'eliminar': EliminarClientes(self.controller, lambda: self.cambiar_vista('menu')),
            'actualizar': ActualizarClientes(self.controller, lambda: self.cambiar_vista('menu')),
            'buscar': BuscarClientes(self.controller, lambda: self.cambiar_vista('menu')),
        }
        for v in self.ventanas.values():
            self.stacked.addWidget(v)
        self.stacked.setCurrentWidget(self.menu)

    def cambiar_vista(self, vista):
        if vista == 'menu':
            self.stacked.setCurrentWidget(self.menu)
        else:
            self.stacked.setCurrentWidget(self.ventanas[vista])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainClientes()
    ventana.show()
    app.exec()
