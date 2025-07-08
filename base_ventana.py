from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

from controlador.cliente_controlador import ClienteControlador

class BaseVentana(QWidget):
    def __init__(self, stacked_widget, titulo, accion, boton_texto, mostrar_buscar=True):
        super().__init__()
        self.controlador = ClienteControlador()
        self.stacked_widget = stacked_widget
        self.titulo_texto = titulo
        self.accion = accion
        self.boton_texto = boton_texto
        self.mostrar_buscar = mostrar_buscar
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #4d5a62; color: white;")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(14)

        titulo = QLabel(self.titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 18px; color: white;")
        layout.addWidget(titulo)

        self.inputs = {}
        campos = ["Identificación", "Nombre", "Correo", "Telefono", "Direccion"]
        for campo in campos:
            label = QLabel(campo)
            label.setStyleSheet("font-weight: 600; margin-bottom: 6px; color: white; font-size: 14px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            edit = QLineEdit()
            edit.setPlaceholderText(campo)
            edit.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 14px;
                color: black;
            """)
            edit.setFixedWidth(450)
            edit.setMinimumHeight(32)

            input_layout = QHBoxLayout()
            input_layout.addStretch()
            input_layout.addWidget(edit)
            input_layout.addStretch()
            layout.addWidget(label)
            layout.addLayout(input_layout)

            self.inputs[campo.lower()] = edit

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(14)

        btn_accion = QPushButton(self.boton_texto)
        btn_accion.clicked.connect(self.ejecutar_accion)
        btn_accion.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        botones_layout.addWidget(btn_accion)

        if self.mostrar_buscar and self.accion != "buscar":
            btn_buscar = QPushButton("Buscar")
            btn_buscar.clicked.connect(self.buscar_cliente)
            btn_buscar.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
            botones_layout.addWidget(btn_buscar)

        btn_otro = QPushButton(f"{self.boton_texto} otro cliente")
        btn_otro.clicked.connect(self.limpiar_campos)
        btn_otro.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        botones_layout.addWidget(btn_otro)

        layout.addSpacing(50)
        layout.addLayout(botones_layout)

        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_inicio)
        btn_regresar.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def limpiar_campos(self):
        for input in self.inputs.values():
            input.clear()

    def volver_inicio(self):
        self.limpiar_campos()
        self.stacked_widget.setCurrentIndex(0)

    def ejecutar_accion(self):
        self.controlador.ejecutar_accion(self.accion, self.inputs, self)

    def buscar_cliente(self):
        self.controlador.buscar_cliente(self.inputs, self)
