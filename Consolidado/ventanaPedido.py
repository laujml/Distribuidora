from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QStackedLayout, QSizePolicy
)
from PyQt6.QtCore import Qt

from Controlador.Pedido.controladorCrearPedido import ControladorCrearPedidos
from Controlador.Pedido.controladorEditPedido import ControladorEditarPedidos
from Controlador.Pedido.controladorVerPedido import VerPedidosControlador

class VentanaPedidos(QWidget):
    def __init__(self):
        super().__init__()        
        # Stack de páginas
        self.stack = QStackedLayout()
        
        # Página principal (menú)
        self.pagina_menu = QWidget()
        layout_menu = QVBoxLayout()
        
        self.titulo = QLabel("Pedidos")
        self.titulo.setObjectName("titulo")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_crear = QPushButton("Crear Pedido")
        btn_crear.clicked.connect(self.mostrar_crear_pedido)
        
        btn_ver = QPushButton("Ver y Cancelar Pedidos")
        btn_ver.clicked.connect(self.mostrar_ver_pedido)
        
        btn_editar = QPushButton("Editar Pedidos")
        btn_editar.clicked.connect(self.mostrar_editar_pedido)
        
        layout_menu.addWidget(self.titulo)
        layout_menu.addWidget(btn_crear)
        layout_menu.addWidget(btn_ver)
        layout_menu.addWidget(btn_editar)
        
        self.pagina_menu.setLayout(layout_menu)
        
        # Controladores
        self.controlador_crear = ControladorCrearPedidos()
        self.pagina_crear = self.controlador_crear.get_vista()
        self.pagina_crear.btn_regresar.clicked.connect(self.volver_menu)
        
        self.controlador_ver = VerPedidosControlador()
        self.pagina_ver_pedidos = self.controlador_ver.get_vista()
        self.pagina_ver_pedidos.btn_regresar.clicked.connect(self.volver_menu)
        
        self.controlador_editar = ControladorEditarPedidos()
        self.pagina_editar = self.controlador_editar.get_vista()
        self.pagina_editar.btn_regresar.clicked.connect(self.volver_menu)
        
        # Agregar páginas al stack
        self.stack.addWidget(self.pagina_menu)
        self.stack.addWidget(self.pagina_crear)
        self.stack.addWidget(self.pagina_ver_pedidos)
        self.stack.addWidget(self.pagina_editar)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stack)
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def mostrar_crear_pedido(self):
        self.controlador_crear = ControladorCrearPedidos()
        self.pagina_crear = self.controlador_crear.get_vista()
        self.pagina_crear.btn_regresar.clicked.connect(self.volver_menu)

        self.stack.insertWidget(1, self.pagina_crear)
        self.stack.setCurrentWidget(self.pagina_crear)

    def mostrar_editar_pedido(self):
        self.controlador_editar = ControladorEditarPedidos()  # ← Nueva instancia cada vez
        self.pagina_editar = self.controlador_editar.get_vista()
        self.pagina_editar.btn_regresar.clicked.connect(self.volver_menu)

        self.stack.insertWidget(3, self.pagina_editar)
        self.stack.setCurrentWidget(self.pagina_editar)

    def mostrar_ver_pedido(self):
        # Eliminar la vista anterior del stack
        self.stack.removeWidget(self.pagina_ver_pedidos)
        self.pagina_ver_pedidos.deleteLater()

        # Crear una nueva instancia del controlador
        self.controlador_ver = VerPedidosControlador()
        self.pagina_ver_pedidos = self.controlador_ver.get_vista()
        self.pagina_ver_pedidos.btn_regresar.clicked.connect(self.volver_menu)

        # Agregar la nueva vista al stack
        self.stack.addWidget(self.pagina_ver_pedidos)
        self.stack.setCurrentWidget(self.pagina_ver_pedidos)

    def volver_menu(self):
        self.stack.setCurrentWidget(self.pagina_menu)

if __name__ == "__main__":
    app = QApplication([])
    window = VentanaPedidos()
    window.resize(800, 600)
    window.show()
    app.exec()
