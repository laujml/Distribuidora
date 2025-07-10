from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from recursos.Styles import Styles
from datetime import datetime

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.periodo = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.titulo = QLabel("Reporte")
        Styles.apply_styles(self.titulo)
        layout.addWidget(self.titulo)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        Styles.apply_styles(self.tabla)
        layout.addWidget(self.tabla)

        self.btn_exportar = QPushButton("Exportar a Excel")
        Styles.apply_styles(self.btn_exportar)
        layout.addWidget(self.btn_exportar)

        self.btn_actualizar = QPushButton("Actualizar Base de Datos")
        Styles.apply_styles(self.btn_actualizar)
        layout.addWidget(self.btn_actualizar)

        layout.addStretch()
        self.setLayout(layout)

    def set_periodo(self, periodo):
        self.periodo = periodo
        self.titulo.setText(f"Reporte {periodo}")

    def actualizar_tabla(self, datos):
        self.tabla.setRowCount(len(datos))
        for row, (fecha, cliente, producto, cantidad, subtotal) in enumerate(datos):
            self.tabla.setItem(row, 0, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(row, 1, QTableWidgetItem(cliente))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(row, 4, QTableWidgetItem(str(subtotal)))

    def actualizar_grafico_ventas(self, fechas, totales):
        self.ax.clear()
        self.ax.plot(fechas, totales, color='#969fa3')
        self.ax.set_facecolor('#4d5a62')
        self.figure.set_facecolor('#4d5a62')
        self.ax.tick_params(colors='#969fa3')
        self.ax.spines['bottom'].set_color('#676d71')
        self.ax.spines['top'].set_color('#676d71')
        self.ax.spines['left'].set_color('#676d71')
        self.ax.spines['right'].set_color('#676d71')
        self.canvas.draw()

    def actualizar_grafico_top_clientes(self, clientes, totales):
        self.ax.clear()
        self.ax.bar(clientes, totales, color='#969a9a')
        self.ax.set_facecolor('#4d5a62')
        self.figure.set_facecolor('#4d5a62')
        self.ax.tick_params(colors='#969fa3')
        self.ax.spines['bottom'].set_color('#676d71')
        self.ax.spines['top'].set_color('#676d71')
        self.ax.spines['left'].set_color('#676d71')
        self.ax.spines['right'].set_color('#676d71')
        self.canvas.draw()

    def actualizar_grafico_productos(self, productos, cantidades):
        self.ax.clear()
        self.ax.barh(productos, cantidades, color='#969a9a')
        self.ax.set_facecolor('#4d5a62')
        self.figure.set_facecolor('#4d5a62')
        self.ax.tick_params(colors='#969fa3')
        self.ax.spines['bottom'].set_color('#676d71')
        self.ax.spines['top'].set_color('#676d71')
        self.ax.spines['left'].set_color('#676d71')
        self.ax.spines['right'].set_color('#676d71')
        self.canvas.draw()