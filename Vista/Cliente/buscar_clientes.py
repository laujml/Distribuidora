# imports
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from Recursos.Styles import Styles

class BuscarClientes(QWidget):
    def __init__(self, controller, regresar_callback=None):
        super().__init__()
        # init
        self.controller = controller
        self.regresar_callback = regresar_callback
        self.setWindowTitle("Buscar clientes")
        self.setMinimumSize(500, 500)
        self.initUI()

    def get_labels(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return ["Identificación", "Nombre", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return "Buscar clientes"

    def get_texto_boton_otro(self):
        """Método que puede ser sobrescrito por clases hijas"""
        return "Buscar otro cliente"

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

        # buscar btn
        btn_buscar = QPushButton("Buscar")
        btn_buscar.setObjectName("btn_primary")
        btn_buscar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_buscar.clicked.connect(self.buscar_item)

        # otro btn
        btn_otro = QPushButton(self.get_texto_boton_otro())
        btn_otro.setObjectName("btn_primary")
        btn_otro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_otro.clicked.connect(self.limpiar_campos)

        # add buttons
        botones_layout.addWidget(btn_buscar)
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
    def buscar_item(self):
        """Método genérico para buscar - debe ser sobrescrito por clases hijas"""
        return self.buscar_cliente()

    # buscar cliente (implementación original)
    def buscar_cliente(self):
        id_cliente = self.campos["Identificación"].text().strip()
        ok, msg, cliente = self.controller.buscar_cliente(id_cliente)
        self.mostrar_popup(msg, ok)
        if ok and cliente:
            # llenar campos
            self.campos["Nombre"].setText(cliente["Nombre"])
            self.campos["Correo"].setText(cliente["Correo"])
            self.campos["Telefono"].setText(cliente["Telefono"])
            self.campos["Direccion"].setText(cliente["Direccion"])
        else:
            self.limpiar_campos()
            self.campos["Identificación"].setText(id_cliente)

    # mostrar popup
    def mostrar_popup(self, mensaje, exito):
        mbox = QMessageBox(self)
        mbox.setWindowTitle("Éxito" if exito else "Error")
        mbox.setText(mensaje)
        mbox.setIcon(QMessageBox.Icon.Information if exito else QMessageBox.Icon.Critical)
        mbox.exec()
