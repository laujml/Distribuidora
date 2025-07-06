from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, 
    QHBoxLayout, QLabel, QComboBox, QSpinBox,QPushButton,
    QTableWidgetItem, QMessageBox, QInputDialog, QDoubleSpinBox, QLineEdit, QFormLayout)

from modelo import Modelo

class VerPedido(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ver pedidos hechos")
        self.modelo = Modelo()
        self.datosPedido()
        #self.verTabla()

    def datosPedido(self):
        self.layoutPrincipal = QVBoxLayout()
        self.layoutLabel = QHBoxLayout()
        
        fecha = QLabel("Fecha: ")    
        dato_Fecha = QLabel("")
        self.layoutLabel.addWidget(fecha)
        self.layoutLabel.addWidget(dato_Fecha)

        numpedido = QLabel("No. de pedido: ")
        dato_Ncumpedido = QLabel("")
        self.layoutLabel.addWidget(numpedido)
        self.layoutLabel.addWidget(dato_Ncumpedido)

        idcliente = QLabel("Ident. del cliente: ")
        dato_IDCliente = QLabel("")
        self.layoutLabel.addWidget(idcliente)
        self.layoutLabel.addWidget(dato_IDCliente)

        nombreCliente = QLabel("Nombre: ")
        dato_nombreCliente = QLabel("")
        self.layoutLabel.addWidget(nombreCliente)
        self.layoutLabel.addWidget(dato_nombreCliente)

        self.layoutPrincipal.addLayout(self.layoutLabel)

    #def verTabla(self):
        self.tabla = QTableWidget(0, 5) #"Crea una tabla vacia, sin filas todavia, pero con 4 columnas ya definidas. Son como "dimensiones" de la tabla inciales.
        self.tabla.setHorizontalHeaderLabels(["Codigo","Producto", "Precio", "Cantidad", "Subtotal"])
        self.layoutPrincipal.addWidget(self.tabla) 

        self.label_total = QLabel("Total: $0.00")
        self.layoutPrincipal.addWidget(self.label_total)

        self.layoutLabelestado = QHBoxLayout()
        self.label_estado = QLabel("Estado: ")
        self.label_pendiente_pagar = QLabel("Monto pendiente: ")
        self.label_plazo_dias = QLabel("Plazo de dias para pagar: ")
        self.layoutLabelestado.addWidget(self.label_estado)
        self.layoutLabelestado.addWidget(self.label_pendiente_pagar)
        self.layoutLabelestado.addWidget(self.label_plazo_dias)
        self.layoutPrincipal.addLayout(self.layoutLabelestado)

        self.setLayout(self.layoutPrincipal)

if __name__ == "__main__":
    app = QApplication([])
    window = VerPedido()
    window.resize(400, 300)
    window.show()
    app.exec()    