from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class MenuPrincipalView(QWidget):
    """Vista del menú principal de productos"""

    def __init__(self, stacked_widget, controlador):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controlador = controlador
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(100, 100, 450, 500)
        self.acciones_vistas = {
            "Agregar producto": 1,
            "Eliminar producto": 2,
            "Ver productos": 3,
            "Actualizar producto": 4
        }
        self.configurar_interfaz()

    def configurar_interfaz(self):
        layout = QVBoxLayout()

        titulo = QLabel("Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        for texto in self.acciones_vistas:
            btn = QPushButton(texto)
            btn.setObjectName(texto)
            btn.clicked.connect(self.manejar_click)
            btn.setFixedHeight(35)
            layout.addWidget(btn)

        self.setLayout(layout)

    def manejar_click(self):
        boton = self.sender()
        texto_boton = boton.objectName()
        indice_vista = self.acciones_vistas.get(texto_boton)
        if indice_vista is not None:
            self.controlador.navegar_a_vista(indice_vista)
