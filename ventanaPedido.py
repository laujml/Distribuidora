import crearPedido

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

        btn2 = QPushButton("Editar Pedido")
        btn2.clicked.connect(self.conectarEditarPedido)

        btn3 = QPushButton("Cancelar Pedido")
        btn3.clicked.connect(self.conectarCancelarPedido)

        btn4 = QPushButton("Ver Pedidos Hechos")
        btn4.clicked.connect(self.conectarVerPedido)

        btn5 = QPushButton("Regresar a menu")
        btn5.clicked.connect(self.regresar)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)    

    def conectarCrearPedido (self):
        self.crear = crearPedido.CrearPedidos()
        self.crear.show()

    def conectarVerPedido (self):
        return     

    def conectarEditarPedido (self):
        return   
    
    def conectarCancelarPedido (self):
        return

    
    def regresar (self):
        return 

if __name__ == "__main__":
    app = QApplication([])
    window = VentanaPedidos()
    window.resize(400, 300)
    window.show()
    app.exec()