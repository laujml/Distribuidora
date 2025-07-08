from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt

class VentanaPrincipal(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(100, 100, 750, 500)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #4d5a62; color: white;")

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(100, 100, 100, 100)
        layout_principal.setSpacing(100)

        titulo = QLabel("Gestión de Clientes")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        layout_principal.addWidget(titulo)

        layout_principal.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        grid_layout = QVBoxLayout()
        grid_layout.setSpacing(15)

        fila1 = QHBoxLayout()
        fila2 = QHBoxLayout()

        botones = [
            ("Agregar cliente", lambda: self.stacked_widget.setCurrentIndex(1)),
            ("Eliminar cliente", lambda: self.stacked_widget.setCurrentIndex(2)),
            ("Actualizar cliente", lambda: self.stacked_widget.setCurrentIndex(3)),
            ("Buscar cliente", lambda: self.stacked_widget.setCurrentIndex(4)),
        ]

        for i, (texto, funcion) in enumerate(botones):
            btn = QPushButton(texto)
            btn.clicked.connect(funcion)
            btn.setFixedHeight(130)
            btn.setFixedWidth(250)
            btn.setStyleSheet("background-color: white; color: black; border-radius: 12px; font-size: 15px; font-weight: 600; padding-top: 90px; padding-bottom: 10px;")
            if i < 2:
                fila1.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            else:
                fila2.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        grid_layout.addLayout(fila1)
        grid_layout.addLayout(fila2)
        layout_principal.addLayout(grid_layout)
        layout_principal.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout_principal)
