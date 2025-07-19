#Se hace uso de PyQt6, Vista.los 3 dialogos "crear, modificar y eliminar usuario"
# La interfaz del administrador contiene acciones que unicamente queremos que las personas con el rol de "administrador" puedan realizar.
# Se realiza unicamente la parte vizual por medio de botones que diriguen a los dialogos antes mencionados o cerrar sesion que pide la confirmacion de "si o no"
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
        #Creaciones de botones con crear, modificar, eliminar o cierre de sesion
        btn_crear = QPushButton("Crear nuevo usuario")
        btn_modificar = QPushButton("Modificar usuario")
        btn_eliminar = QPushButton("Eliminar usuario")
        btn_cerrar = QPushButton("Cerrar sesión")
        
        # Conectar eventos con los botones
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
    #Son funciones que crean y ejecutan los dialogos correspondientes
    def crear_usuario(self):
        dialog = CrearUsuarioDialog()
        dialog.exec()
    
    def modificar_usuario(self):
        dialog = ModificarUsuarioDialog()
        dialog.exec()
    
    def eliminar_usuario(self):
        dialog = EliminarUsuarioDialog()
        dialog.exec()
    #Cierre de sesion
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
