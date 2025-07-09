import Vista.crearPedido as crearPedido
import Vista.verPedidos as verPedidos
import Vista.editarPedido as editarPedido

from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout,
    QLabel)

from PyQt6.QtCore import Qt

class VentanaPedidos (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pedidos") 

        titulo = QLabel("Pedidos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn1 = QPushButton("Crear Pedido")
        btn1.clicked.connect(self.conectarCrearPedido)

        btn2 = QPushButton("Ver y cancelar Pedidos")
        btn2.clicked.connect(self.conectarVerPedido)

        btn3 = QPushButton("Editar Pedidos")
        btn3.clicked.connect(self.conectarEditarPedidos)

        btn5 = QPushButton("Regresar a menu")
        btn5.clicked.connect(self.regresar)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)    

    def conectarCrearPedido (self):
        self.crear = crearPedido.CrearPedidos()
        self.crear.btn_regresar.clicked.connect(self.volver_de_crear)
        self.crear.show()
        self.hide()

    def volver_de_crear(self):
        self.crear.close() 
        self.show()    

    def conectarVerPedido (self):
        self.ver_pedidos = verPedidos.VerPedidos()
        self.ver_pedidos.resize(800, 600)
        self.ver_pedidos.show()

    def conectarEditarPedidos(self):
        self.editar_pedidos = editarPedido.EditarPedido() 
        self.editar_pedidos.formulario.btn_regresar.clicked.connect(self.volver_de_editar)
        self.editar_pedidos.show()
        self.hide()

    def volver_de_editar(self):
        self.editar_pedidos.close() 
        self.show()        

    def regresar (self):
        return 

if __name__ == "__main__":
    app = QApplication([])
    window = VentanaPedidos()
    window.resize(400, 300)
    window.show()
    app.exec()