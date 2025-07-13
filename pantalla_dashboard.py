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
            "Clientes", "Pedidos", "Productos", 
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

        self.setStyleSheet("""
            /* Fondo principal */
            PantallaDashboard {
                background-color: #4d5a62;
            }
            
            /* Panel de contenido - completamente transparente */
            QWidget#panelContenido {
                background-color: transparent;
                border: none;
            }
            
            /* Tarjetas blancas con estilos internos */
            QFrame#tarjeta {
                background-color: white;
                border-radius: 20px;
                padding: 25px;
                min-width: 300px;
                border: 1px solid #e0e0e0;
            }
            
            /* Todos los labels dentro de tarjetas */
            QFrame#tarjeta QLabel {
                background-color: white; 
                color: #4d5a62;        
                border: none;            
                padding: 0;              
                margin: 0;               
            }
            
            /* Títulos de sección */
            QLabel#titulo {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 30px;
                background-color: transparent;
            }
            /* Botón con hover */
            QPushButton {
                background-color: white;
                color: #4d5a62;
                border: 2px solid #4d5a62;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 180px;
            }
    
            QPushButton:hover {
                background-color: #f0f0f0;  /* Gris muy claro al pasar mouse */
            }
    
            QPushButton:pressed {
                background-color: #e0e0e0;  
                border: 2px solid #3a454b;  
            }

            /* Texto dentro de tarjetas blancas */
            QFrame#tarjeta QLabel {
                background-color: white;
                color: #4d5a62;
                font-size: 16px;
                font-weight: bold;
                padding: 2px 0;
                margin: 0;
            }
    
            /* Títulos de sección dentro de tarjetas */
            QFrame#tarjeta QLabel#subtitulo {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            /* Valores numéricos */
            QFrame#tarjeta QLabel#dato {
                font-size: 20px;
                margin: 5px 0 15px 0;
            }
            
            /* Items de inventario */
            QFrame#tarjeta QLabel#dato_inventario {
                font-size: 16px;
                margin: 4px 0;
            }
        """)
        
        
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
