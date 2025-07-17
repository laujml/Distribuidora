from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from Vista.Usuario.dialogo_crear_usuario import CrearUsuarioDialog
from Vista.Usuario.dialogo_modificar_usuario import ModificarUsuarioDialog
from Vista.Usuario.dialogo_eliminar_usuario import EliminarUsuarioDialog

class PantallaAdministrador(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        
        titulo = QLabel("Panel de Administrador")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_crear = QPushButton("Crear nuevo usuario")
        btn_modificar = QPushButton("Modificar usuario")
        btn_eliminar = QPushButton("Eliminar usuario")
        btn_cerrar = QPushButton("Cerrar sesión")
        
        # Conectar eventos
        btn_crear.clicked.connect(self.crear_usuario)
        btn_modificar.clicked.connect(self.modificar_usuario)
        btn_eliminar.clicked.connect(self.eliminar_usuario)
        btn_cerrar.clicked.connect(self.confirmar_cierre)
        
        layout.addWidget(titulo)
        layout.addWidget(btn_crear)
        layout.addWidget(btn_modificar)
        layout.addWidget(btn_eliminar)
        layout.addWidget(btn_cerrar)
        
        self.setLayout(layout)
    
    def crear_usuario(self):
        dialog = CrearUsuarioDialog()
        dialog.exec()
    
    def modificar_usuario(self):
        dialog = ModificarUsuarioDialog()
        dialog.exec()
    
    def eliminar_usuario(self):
        dialog = EliminarUsuarioDialog()
        dialog.exec()
    
    def confirmar_cierre(self):
        confirm = QMessageBox.question(
            self, "Cerrar sesión", 
            "¿Desea cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            # Obtener referencia al contenedor principal
            contenedor = self.stack.parent()
            if hasattr(contenedor, 'cerrar_sesion'):
                contenedor.cerrar_sesion()
            else:
                self.stack.setCurrentIndex(0)
