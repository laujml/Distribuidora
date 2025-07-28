# imports
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Recursos.Styles import Styles

class AgregarClientes(QWidget):
    def __init__(self, controller, regresar_callback=None):
        super().__init__()
        # init
        self.controller = controller
        self.regresar_callback = regresar_callback
        self.setWindowTitle("Agregar clientes")
        self.setMinimumSize(500, 500)
        self.initUI()

    def get_labels(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return ["Identificación", "Nombre", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return "Agregar clientes"

    def get_texto_boton_otro(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return "Agregar otro cliente"

    def initUI(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # titulo
        titulo_ventana = QLabel(self.get_titulo_ventana())
        titulo_ventana.setObjectName("titulo")
        titulo_ventana.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(titulo_ventana)

        # form widget
        self.form_widget = QWidget()
        self.form_widget.setObjectName("form_widget")
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # campos dict
        self.campos = {}
        
        # crear campos usando el método get_labels()
        labels = self.get_labels()
        for i, campo in enumerate(labels):
            label = QLabel(campo)
            label.setObjectName("campo_label")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.form_layout.addWidget(label)
            
            input_ = QLineEdit()
            input_.setObjectName("campo_input")
            input_.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.form_layout.addWidget(input_)
            self.campos[campo] = input_
            
            if i == len(labels) - 1:
                self.form_layout.addSpacing(24)

        # buttons layout
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        # guardar btn
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setObjectName("btn_primary")
        btn_guardar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_guardar.clicked.connect(self.guardar_item)

        # otro btn
        btn_otro = QPushButton(self.get_texto_boton_otro())
        btn_otro.setObjectName("btn_primary")
        btn_otro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_otro.clicked.connect(self.limpiar_campos)

        # add buttons
        botones_layout.addWidget(btn_guardar)
        botones_layout.addWidget(btn_otro)
        self.form_layout.addLayout(botones_layout)

        # regresar btn
        btn_regresar = QPushButton("← Regresar")
        btn_regresar.setObjectName("btn_secondary")
        btn_regresar.setMaximumWidth(140)
        btn_regresar.clicked.connect(self.regresar)
        self.form_layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    # limpiar campos
    def limpiar_campos(self):
        for campo in self.campos.values():
            campo.clear()

    # regresar
    def regresar(self):
        self.limpiar_campos()
        if self.regresar_callback:
            self.regresar_callback()

    # Método genérico que puede ser sobrescrito
    def guardar_item(self):
        """Método genérico para guardar - debe ser sobrescrito por clases hijas"""
        return self.guardar_cliente()

    # guardar cliente (implementación original)
    def guardar_cliente(self):
        # obtener datos
        id_cliente = self.campos["Identificación"].text().strip()
        if not id_cliente.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        nombre = self.campos["Nombre"].text().strip()
        correo = self.campos["Correo"].text().strip()
        telefono = self.campos["Telefono"].text().strip()
        direccion = self.campos["Direccion"].text().strip()
        ok, msg = self.controller.agregar_cliente(id_cliente, nombre, correo, telefono, direccion)
        self.mostrar_popup(msg, ok)

    # mostrar popup
    def mostrar_popup(self, mensaje, exito):
        mbox = QMessageBox(self)
        mbox.setWindowTitle("Éxito" if exito else "Error")
        mbox.setText(mensaje)
        mbox.setIcon(QMessageBox.Icon.Information if exito else QMessageBox.Icon.Critical)
        mbox.exec()
