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
        self.setStyleSheet("background-color: #4d5a62;")
        self.font = QFont("Poppins", 14)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # Título principal
        titulo = QLabel("Clientes")
        titulo.setFont(QFont("Poppins", 38, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #fff; margin-bottom: 32px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(titulo)

        # Botones en grid 2x2
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(60)
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        col1.setSpacing(32)
        col2.setSpacing(32)

        estilo_boton = """
            QToolButton {
                background: #fff;
                color: #222;
                border-radius: 28px;
                padding: 16px 32px;
                font-size: 1.15rem;
                font-family: 'Poppins', sans-serif;
                font-weight: 500;
                min-width: 260px;
                min-height: 120px;
            }
        """

        btn_agregar = QToolButton()
        btn_agregar.setText("Agregar cliente")
        btn_agregar.setIcon(QIcon("recursos/Agregar cliente.jpg"))
        btn_agregar.setIconSize(QSize(72, 72))
        btn_agregar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn_agregar.setFont(QFont("Poppins", 20, QFont.Weight.Medium))
        btn_agregar.setStyleSheet(estilo_boton)
        btn_agregar.clicked.connect(lambda: self.cambiar_vista('agregar'))

        btn_actualizar = QToolButton()
        btn_actualizar.setText("Actualizar cliente")
        btn_actualizar.setIcon(QIcon("recursos/Actualizar datos.jpg"))
        btn_actualizar.setIconSize(QSize(72, 72))
        btn_actualizar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn_actualizar.setFont(QFont("Poppins", 20, QFont.Weight.Medium))
        btn_actualizar.setStyleSheet(estilo_boton)
        btn_actualizar.clicked.connect(lambda: self.cambiar_vista('actualizar'))

        btn_eliminar = QToolButton()
        btn_eliminar.setText("Eliminar cliente")
        btn_eliminar.setIcon(QIcon("recursos/Eliminar cliente.jpg"))
        btn_eliminar.setIconSize(QSize(72, 72))
        btn_eliminar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn_eliminar.setFont(QFont("Poppins", 20, QFont.Weight.Medium))
        btn_eliminar.setStyleSheet(estilo_boton)
        btn_eliminar.clicked.connect(lambda: self.cambiar_vista('eliminar'))

        btn_buscar = QToolButton()
        btn_buscar.setText("Buscar cliente")
        btn_buscar.setIcon(QIcon("recursos/Buscar.jpg"))
        btn_buscar.setIconSize(QSize(72, 72))
        btn_buscar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn_buscar.setFont(QFont("Poppins", 20, QFont.Weight.Medium))
        btn_buscar.setStyleSheet(estilo_boton)
        btn_buscar.clicked.connect(lambda: self.cambiar_vista('buscar'))

        col1.addWidget(btn_agregar)
        col1.addWidget(btn_eliminar)
        col2.addWidget(btn_actualizar)
        col2.addWidget(btn_buscar)
        grid_layout.addLayout(col1)
        grid_layout.addLayout(col2)
        main_layout.addLayout(grid_layout)

class MainClientes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clientes")
        self.setStyleSheet("background-color: #4d5a62;")
        self.setMinimumSize(900, 600)
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
    sys.exit(app.exec()) 
