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
        self.setStyleSheet(Styles.global_stylesheet())
        self.setMinimumSize(500, 500)
        self.font = QFont("Poppins", 11)
        self.initUI()

    def initUI(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # titulo
        titulo_ventana = QLabel("Buscar clientes")
        titulo_ventana.setFont(QFont("Poppins", 22, QFont.Weight.Bold))
        titulo_ventana.setStyleSheet("color: #fff; margin-top: 18px; margin-bottom: 18px;")
        titulo_ventana.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(titulo_ventana)

        # form widget
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # campos dict
        self.campos = {}
        input_height = 38
        border_radius_input = 19
        # input style
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
        # crear campos
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

        # buttons layout
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        border_radius_btn = 12
        # button style
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
        # buscar btn
        btn_buscar = QPushButton("Buscar")
        btn_buscar.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_buscar.setStyleSheet(estilo_boton)
        btn_buscar.setMinimumHeight(input_height)
        btn_buscar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_buscar.clicked.connect(self.buscar_cliente)

        # otro btn
        btn_otro = QPushButton("Buscar otro cliente")
        btn_otro.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_otro.setStyleSheet(estilo_boton)
        btn_otro.setMinimumHeight(input_height)
        btn_otro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_otro.clicked.connect(self.limpiar_campos)

        # add buttons
        botones_layout.addWidget(btn_buscar)
        botones_layout.addWidget(btn_otro)
        self.form_layout.addLayout(botones_layout)

        # regresar btn
        btn_regresar = QPushButton("← Regresar")
        btn_regresar.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        btn_regresar.setStyleSheet(estilo_boton)
        btn_regresar.setMinimumHeight(input_height)
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

    # buscar cliente
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

if __name__ == "__main__":
    # main
    app = QApplication(sys.argv)
    ventana = BuscarClientes()
    ventana.show()
    sys.exit(app.exec())
