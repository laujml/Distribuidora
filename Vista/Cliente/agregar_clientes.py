from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Recursos.Styles import Styles

class AgregarClientes(QWidget):
    def __init__(self, controller, regresar_callback=None):
        super().__init__()
        self.controller = controller
        self.regresar_callback = regresar_callback
        self.setWindowTitle("Agregar clientes")
        self.setStyleSheet(Styles.global_stylesheet())
        self.setMinimumSize(500, 500)
        self.font = QFont("Poppins", 11)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        titulo_ventana = QLabel("Agregar clientes")
        titulo_ventana.setFont(QFont("Poppins", 22, QFont.Weight.Bold))
        titulo_ventana.setStyleSheet("color: #fff; margin-top: 18px; margin-bottom: 18px;")
        titulo_ventana.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(titulo_ventana)

        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.campos = {}
        input_height = 38
        border_radius_input = 19
        estilo_input = f"""
            QLineEdit {{
                background: #fff;
                border-radius: {border_radius_input}px;
                border: none;
                padding: 6px 16px;
                font-size: 1rem;
                font-family: 'Poppins', sans-serif;
            }}
        """
        labels = ["Identificación", "Nombre", "Correo", "Telefono", "Direccion"]
        for i, campo in enumerate(labels):
            label = QLabel(campo)
            label.setFont(QFont("Poppins", 12, QFont.Weight.Medium))
            label.setStyleSheet("color: #fff; margin-bottom: 2px;")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.form_layout.addWidget(label)
            input_ = QLineEdit()
            input_.setFont(self.font)
            input_.setStyleSheet(estilo_input)
            input_.setMinimumHeight(input_height)
            input_.setMaximumHeight(input_height)
            input_.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.form_layout.addWidget(input_)
            self.campos[campo] = input_
            if i == len(labels) - 1:
                self.form_layout.addSpacing(24)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        border_radius_btn = 12
        estilo_boton = f"""
            QPushButton {{
                background: #fff;
                color: #222;
                border-radius: {border_radius_btn}px;
                padding: 6px 18px;
                font-size: 1rem;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
            }}
            QPushButton:hover {{
                background-color: #eaeaea;
            }}
        """
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_guardar.setStyleSheet(estilo_boton)
        btn_guardar.setMinimumHeight(input_height)
        btn_guardar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_guardar.clicked.connect(self.guardar_cliente)

        btn_otro = QPushButton("Agregar otro cliente")
        btn_otro.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_otro.setStyleSheet(estilo_boton)
        btn_otro.setMinimumHeight(input_height)
        btn_otro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_otro.clicked.connect(self.limpiar_campos)

        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_otro)
        self.form_layout.addLayout(botones_layout)

        btn_regresar = QPushButton("← Regresar")
        btn_regresar.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_regresar.setStyleSheet(estilo_boton)
        btn_regresar.setMinimumHeight(input_height)
        btn_regresar.setMaximumWidth(140)
        btn_regresar.clicked.connect(self.regresar)
        self.form_layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def limpiar_campos(self):
        for campo in self.campos.values():
            campo.clear()

    def regresar(self):
        self.limpiar_campos()
        if self.regresar_callback:
            self.regresar_callback()

    def guardar_cliente(self):
        id_cliente = self.campos["Identificación"].text().strip()
        nombre = self.campos["Nombre"].text().strip()
        correo = self.campos["Correo"].text().strip()
        telefono = self.campos["Telefono"].text().strip()
        direccion = self.campos["Direccion"].text().strip()
        ok, msg = self.controller.agregar_cliente(id_cliente, nombre, correo, telefono, direccion)
        self.mostrar_popup(msg, ok)

    def mostrar_popup(self, mensaje, exito):
        mbox = QMessageBox(self)
        mbox.setWindowTitle("Éxito" if exito else "Error")
        mbox.setText(mensaje)
        mbox.setIcon(QMessageBox.Icon.Information if exito else QMessageBox.Icon.Critical)
        mbox.exec() 
