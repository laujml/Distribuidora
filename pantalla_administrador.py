from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from vista.dialogo_crear_usuario import CrearUsuarioDialog
from vista.dialogo_modificar_usuario import ModificarUsuarioDialog
from vista.dialogo_eliminar_usuario import EliminarUsuarioDialog

class PantallaAdministrador(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setStyleSheet("""
            QWidget {
                background-color: #4d5a62;
            }
            QLabel#titulo {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 25px; /* Totalmente redondo */
                font-size: 14px;
                min-width: 240px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        titulo = QLabel("Administrador")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_crear = QPushButton("Crear nuevo usuario")
        btn_modificar = QPushButton("Modificar usuario")
        btn_eliminar = QPushButton("Eliminar usuario")
        btn_cerrar = QPushButton("Cerrar sesión")

        btn_crear.clicked.connect(lambda: CrearUsuarioDialog().exec())
        btn_modificar.clicked.connect(lambda: ModificarUsuarioDialog().exec())
        btn_eliminar.clicked.connect(lambda: EliminarUsuarioDialog().exec())
        btn_cerrar.clicked.connect(self.confirmar_cierre)

        layout.addWidget(titulo)
        layout.addWidget(btn_crear)
        layout.addWidget(btn_modificar)
        layout.addWidget(btn_eliminar)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)

    def confirmar_cierre(self):
        confirm = QMessageBox.question(self, "Cerrar sesión", "¿Desea cerrar sesión?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.stack.setCurrentIndex(0)
