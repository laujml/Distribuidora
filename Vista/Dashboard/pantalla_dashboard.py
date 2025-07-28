# Se desarrolla toda la parte visual de la pantalla principal despues de la verificacion del login
# Uso de PyQt6 y Controlador.Dashboard
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QApplication
from PyQt6.QtCore import Qt
import sys
from Controlador.Dashboard.dashboard_controlador import obtener_datos_dashboard
from Recursos.Styles import Styles

class PantallaDashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Panel derecho del dashboard
        self.panel_dashboard = QWidget()
        self.panel_dashboard.setObjectName("panelContenido") 
        self.layout_dashboard = QVBoxLayout(self.panel_dashboard)
        self.layout_dashboard.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout_dashboard.setSpacing(30)
        self.layout_dashboard.setContentsMargins(30, 30, 30, 30)

        layout_principal.addWidget(self.panel_dashboard, 3)

        self.panel_dashboard.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.crear_dashboard()

    # Creacion exclusiva del Dashboard
    def crear_dashboard(self):
        titulo = QLabel("¡Bienvenido!")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_dashboard.addWidget(titulo)

        # INGRESOS: Se desarrolla la seccion de ingresos por medio de tarjetas, definicion de titulos y subtitulos
        ingresos_layout = QHBoxLayout()
        ingresos_layout.setSpacing(30)

        self.lbl_ayer = QLabel("$0.00")
        self.lbl_ayer.setObjectName("dato")
        self.lbl_hoy = QLabel("$0.00")
        self.lbl_hoy.setObjectName("dato")

        tarjeta_ayer = QFrame()
        tarjeta_ayer.setObjectName("tarjeta")
        lyt1 = QVBoxLayout(tarjeta_ayer)
        lyt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt1.setSpacing(15)
        lbl_titulo_ayer = QLabel("Ingresos día anterior")
        lbl_titulo_ayer.setObjectName("subtitulo")
        lbl_titulo_ayer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt1.addWidget(lbl_titulo_ayer)
        lyt1.addWidget(self.lbl_ayer)

        tarjeta_hoy = QFrame()
        tarjeta_hoy.setObjectName("tarjeta")
        lyt2 = QVBoxLayout(tarjeta_hoy)
        lyt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt2.setSpacing(15)
        lbl_titulo_hoy = QLabel("Ingresos día de hoy")
        lbl_titulo_hoy.setObjectName("subtitulo")
        lbl_titulo_hoy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt2.addWidget(lbl_titulo_hoy)
        lyt2.addWidget(self.lbl_hoy)

        ingresos_layout.addWidget(tarjeta_ayer)
        ingresos_layout.addWidget(tarjeta_hoy)
        self.layout_dashboard.addLayout(ingresos_layout)

        # INVENTARIO: Se desarrolla la seccion de inventario por medio de tarjetas y subtitulos
        tarjeta_inv = QFrame()
        tarjeta_inv.setObjectName("tarjeta")
        layout_inv = QVBoxLayout(tarjeta_inv)
        layout_inv.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_inv.setSpacing(15)

        lbl_titulo_inv = QLabel("Estado del inventario")
        lbl_titulo_inv.setObjectName("subtitulo")
        lbl_titulo_inv.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_inv.addWidget(lbl_titulo_inv)
        
        self.lbl_inventario = QLabel()
        self.lbl_inventario.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.lbl_inventario.setWordWrap(True)
        self.lbl_inventario.setObjectName("dato_inventario")
        layout_inv.addWidget(self.lbl_inventario)

        self.layout_dashboard.addWidget(tarjeta_inv)

        # ACTUALIZAR: El boton actualizar tiene el fin de recargar la informacion de la base de datos para que sea reflejado en la base. 
        # Se realiza la conexion al hacer el respectivo click con actualizar_datos
        self.btn_actualizar = QPushButton("Actualizar datos")
        self.btn_actualizar.setObjectName("btn_dashboard")
        self.btn_actualizar.clicked.connect(self.actualizar_datos)
        self.layout_dashboard.addWidget(self.btn_actualizar, alignment=Qt.AlignmentFlag.AlignRight)

        self.actualizar_datos()

    # Se extrae la data por medio de obtener_datos_dashboard, hacemos ajustes a 2 decimales y se puede presentar la informacion
    def actualizar_datos(self):
        datos = obtener_datos_dashboard()
        self.lbl_ayer.setText(f"${datos['ingresos_ayer']:.2f}")
        self.lbl_hoy.setText(f"${datos['ingresos_hoy']:.2f}")

        texto = ""
        for descripcion, stock in datos['inventario']:
            texto += f"{descripcion}: {stock}<br>"
        self.lbl_inventario.setText(texto)

if __name__ == "__main__":
    # main
    app = QApplication(sys.argv)
    app.setStyleSheet(Styles.global_stylesheet())
    ventana = PantallaDashboard(None)
    ventana.show()
    sys.exit(app.exec())
