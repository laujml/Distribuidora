from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QStackedWidget, QToolButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import sys
from Vista.Proveedor.agregar_proveedores import AgregarProveedores
from Vista.Proveedor.buscar_proveedores import BuscarProveedores
from Vista.Proveedor.actualizar_proveedores import ActualizarProveedores
from Vista.Proveedor.eliminar_proveedores import EliminarProveedores
from Controlador.Proveedor.proveedor_controller import ProveedorController

class MenuPrincipal(QWidget):
    def __init__(self, cambiar_vista):
        super().__init__()
        self.cambiar_vista = cambiar_vista
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Proveedores")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        btn_agregar = QPushButton()
        btn_agregar.setText("Agregar proveedor")
        btn_agregar.setIcon(QIcon("recursos/Agregar cliente.jpg"))
        btn_agregar.clicked.connect(lambda: self.cambiar_vista('agregar'))
        main_layout.addWidget(btn_agregar)

        btn_actualizar = QPushButton()
        btn_actualizar.setText("Actualizar datos")
        btn_actualizar.setIcon(QIcon("recursos/Actualizar datos.jpg"))
        btn_actualizar.clicked.connect(lambda: self.cambiar_vista('actualizar'))
        main_layout.addWidget(btn_actualizar)

        btn_eliminar = QPushButton()
        btn_eliminar.setText("Eliminar proveedor")
        btn_eliminar.setIcon(QIcon("recursos/Eliminar cliente.jpg"))
        btn_eliminar.clicked.connect(lambda: self.cambiar_vista('eliminar'))
        main_layout.addWidget(btn_eliminar)

        btn_buscar = QPushButton()
        btn_buscar.setText("Buscar proveedor")
        btn_buscar.setIcon(QIcon("recursos/Buscar.jpg"))
        btn_buscar.clicked.connect(lambda: self.cambiar_vista('buscar'))
        main_layout.addWidget(btn_buscar)

        self.setLayout(main_layout)

class MainProveedores(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        self.controller = ProveedorController()  # Instancia única del controlador
        self.init_vistas()

    def init_vistas(self):
        self.menu = MenuPrincipal(self.cambiar_vista)
        self.stacked.addWidget(self.menu)
        # Instancias de las ventanas de acción, pasando el controlador y el callback
        self.ventanas = {
            'agregar': AgregarProveedores(self.controller, lambda: self.cambiar_vista('menu')),
            'eliminar': EliminarProveedores(self.controller, lambda: self.cambiar_vista('menu')),
            'actualizar': ActualizarProveedores(self.controller, lambda: self.cambiar_vista('menu')),
            'buscar': BuscarProveedores(self.controller, lambda: self.cambiar_vista('menu')),
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
    ventana = MainProveedores()
    ventana.show()
    sys.exit(app.exec()) 
