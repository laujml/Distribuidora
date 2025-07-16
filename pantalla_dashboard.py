from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt
from recursos.menu_lateral import MenuLateral
from controlador.dashboard_controlador import obtener_datos_dashboard


class PantallaDashboard(QWidget):
    def __init__(self, stack, usuario):
        super().__init__()
        self.stack = stack
        self.usuario = usuario

        
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        
        menu_container = QFrame()
        menu_container.setStyleSheet("background-color: white; font-size: 18px;")
        menu_container.setFixedWidth(250)

        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

       menu = MenuLateral(stack=self.stack, opciones=[
            "Dashboard", "Clientes", "Pedidos", "Productos", 
            "Proveedores", "Reportes", "Cerrar sesión"
        ])
        menu_layout.addWidget(menu)
        layout_principal.addWidget(menu_container)

        # Panel derecho del dashboard
        self.panel_dashboard = QWidget()
        self.panel_dashboard.setObjectName("panelContenido") 
        self.layout_dashboard = QVBoxLayout(self.panel_dashboard)
        self.layout_dashboard.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout_dashboard.setSpacing(30)
        self.layout_dashboard.setContentsMargins(30, 30, 30, 30)

        layout_principal.addWidget(self.panel_dashboard, 3)

        self.setStyleSheet(Styles.get_stylesheet() + Styles.get_estilo_dashboard())
        self.panel_dashboard.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.crear_dashboard()

    def crear_dashboard(self):
        titulo = QLabel("¡Bienvenido!")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_dashboard.addWidget(titulo)

        #INGRESOS
        ingresos_layout = QHBoxLayout()
        ingresos_layout.setSpacing(30)

        self.lbl_ayer = QLabel("$0.00")
        self.lbl_ayer.setObjectName("dato")
        self.lbl_hoy = QLabel("$0.00")
        self.lbl_hoy.setObjectName("dato")

        tarjeta_ayer = QFrame(objectName="tarjeta")
        lyt1 = QVBoxLayout(tarjeta_ayer)
        lyt1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt1.setSpacing(15)
        lbl_titulo_ayer = QLabel("Ingresos día anterior", alignment=Qt.AlignmentFlag.AlignCenter)
        lbl_titulo_ayer.setObjectName("subtitulo")
        lyt1.addWidget(lbl_titulo_ayer)
        lyt1.addWidget(self.lbl_ayer)

        tarjeta_hoy = QFrame(objectName="tarjeta")
        lyt2 = QVBoxLayout(tarjeta_hoy)
        lyt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lyt2.setSpacing(15)
        lbl_titulo_hoy = QLabel("Ingresos día de hoy", alignment=Qt.AlignmentFlag.AlignCenter)
        lbl_titulo_hoy.setObjectName("subtitulo")
        lyt2.addWidget(lbl_titulo_hoy)
        lyt2.addWidget(self.lbl_hoy)

        ingresos_layout.addWidget(tarjeta_ayer)
        ingresos_layout.addWidget(tarjeta_hoy)
        self.layout_dashboard.addLayout(ingresos_layout)

        #INVENTARIO
        tarjeta_inv = QFrame(objectName="tarjeta")
        layout_inv = QVBoxLayout(tarjeta_inv)
        layout_inv.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_inv.setSpacing(15)

        lbl_titulo_inv = QLabel("Estado del inventario", alignment=Qt.AlignmentFlag.AlignCenter)
        lbl_titulo_inv.setObjectName("subtitulo")
        layout_inv.addWidget(lbl_titulo_inv)
        
        self.lbl_inventario = QLabel()
        self.lbl_inventario.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.lbl_inventario.setWordWrap(True)
        self.lbl_inventario.setObjectName("dato_inventario")
        layout_inv.addWidget(self.lbl_inventario)

        self.layout_dashboard.addWidget(tarjeta_inv)

        #ACTUALIZAR
        self.btn_actualizar = QPushButton("Actualizar datos")
        self.btn_actualizar.clicked.connect(self.actualizar_datos)
        self.layout_dashboard.addWidget(self.btn_actualizar, alignment=Qt.AlignmentFlag.AlignRight)

        self.actualizar_datos()

    def actualizar_datos(self):
        datos = obtener_datos_dashboard()
        self.lbl_ayer.setText(f"${datos['ingresos_ayer']:.2f}")
        self.lbl_hoy.setText(f"${datos['ingresos_hoy']:.2f}")

        texto = ""
        for descripcion, stock in datos['inventario']:
            texto += f"{descripcion}: {stock}<br>"
        self.lbl_inventario.setText(texto)
