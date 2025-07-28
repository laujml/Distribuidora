# Vista/MenuPrincipalView.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class MenuPrincipalView(QWidget):
    """Vista del menú principal de productos"""
    
    def __init__(self, stacked_widget, controlador):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.controlador = controlador  # Referencia al controlador
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(100, 100, 450, 500)
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz del menú principal"""
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)
        
        # Botones del menú - Ahora delegan al controlador
        botones_config = [
            ("Agregar producto", lambda: self.controlador.navegar_a_vista(1)),
            ("Eliminar producto", lambda: self.controlador.navegar_a_vista(2)),
            ("Ver productos", lambda: self.controlador.navegar_a_vista(3)),
            ("Actualizar producto", lambda: self.controlador.navegar_a_vista(4)),
        ]
        
        for texto, funcion in botones_config:
            btn = QPushButton(texto)
            btn.clicked.connect(funcion)
            btn.setFixedHeight(35)
            layout.addWidget(btn)
        
        self.setLayout(layout)
