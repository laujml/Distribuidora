from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QMessageBox
from PyQt6.QtCore import QTimer

class PantallaDashboard(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Bienvenido")

        layout = QVBoxLayout()
        self.label_bienvenida = QLabel(f"¡Bienvenido {self.usuario['nombre']}!")
        self.label_ingreso_ayer = QLabel()
        self.label_ingreso_hoy = QLabel()
        self.grid_inventario = QGridLayout()

        layout.addWidget(self.label_bienvenida)
        layout.addWidget(QLabel("Ingresos día anterior"))
        layout.addWidget(self.label_ingreso_ayer)
        layout.addWidget(QLabel("Ingresos día de hoy"))
        layout.addWidget(self.label_ingreso_hoy)
        layout.addWidget(QLabel("Estado del inventario"))
        layout.addLayout(self.grid_inventario)
        self.setLayout(layout)

        self.actualizar_datos()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(10000)

        rol = self.usuario.get("rol", "").lower()
        if rol == "cliente":
            self.label_ingreso_ayer.hide()
            self.label_ingreso_hoy.hide()
        elif rol != "administrador":
            QMessageBox.warning(self, "Error", "Rol de usuario desconocido.")
