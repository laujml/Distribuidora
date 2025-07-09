from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableView, QDateEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.apply_styles()

    def apply_styles(self):
        stylesheet = """
            QWidget {
                background-color: #1d222e;
                color: #969fa3;
            }
            QPushButton {
                background-color: #40464b;
                color: #969fa3;
                border: 1px solid #676d71;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #676d71;
            }
            QComboBox, QDateEdit, QTableView {
                background-color: #4d5a62;
                color: #969fa3;
                border: 1px solid #676d71;
            }
            QLabel {
                color: #969a9a;
            }
        """
        self.setStyleSheet(stylesheet)

    def init_ui(self):
        layout = QVBoxLayout()

        # Filtros
        filtros_layout = QHBoxLayout()
        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.cliente_cb = QComboBox()
        self.cliente_cb.addItem("Todos los clientes")
        self.producto_cb = QComboBox()
        self.producto_cb.addItem("Todos los productos")
        self.buscar_btn = QPushButton("Buscar")
        self.limpiar_btn = QPushButton("Limpiar filtros")

        filtros_layout.addWidget(QLabel("Período:"))
        filtros_layout.addWidget(self.period_cb)
        filtros_layout.addWidget(QLabel("Desde:"))
        filtros_layout.addWidget(self.fecha_inicio)
        filtros_layout.addWidget(QLabel("Hasta:"))
        filtros_layout.addWidget(self.fecha_fin)
        filtros_layout.addWidget(QLabel("Cliente:"))
        filtros_layout.addWidget(self.cliente_cb)
        filtros_layout.addWidget(QLabel("Producto:"))
        filtros_layout.addWidget(self.producto_cb)
        filtros_layout.addWidget(self.buscar_btn)
        filtros_layout.addWidget(self.limpiar_btn)
        layout.addLayout(filtros_layout)

        # Resumen
        resumen_layout = QGridLayout()
        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        self.label_producto_top = QLabel("Producto más vendido: -")
        self.label_cliente_top = QLabel("Cliente top: -")
        resumen_layout.addWidget(self.label_total_ventas, 0, 0)
        resumen_layout.addWidget(self.label_total_pedidos, 0, 1)
        resumen_layout.addWidget(self.label_producto_top, 1, 0)
        resumen_layout.addWidget(self.label_cliente_top, 1, 1)
        layout.addLayout(resumen_layout)

        # Gráficos
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Tabla
        self.tabla_resultados = QTableView()
        self.model = QStandardItemModel()
        self.tabla_resultados.setModel(self.model)
        layout.addWidget(self.tabla_resultados)

        # Botones
        botones_layout = QHBoxLayout()
        self.exportar_btn = QPushButton("Exportar a Excel")
        self.actualizar_btn = QPushButton("Actualizar Datos")
        botones_layout.addWidget(self.exportar_btn)
        botones_layout.addWidget(self.actualizar_btn)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def populate_clientes(self, clientes):
        for id_cliente, nombre in clientes:
            self.cliente_cb.addItem(f"{id_cliente} - {nombre}", id_cliente)

    def populate_productos(self, productos):
        for id_producto, desc in productos:
            self.producto_cb.addItem(f"{id_producto} - {desc}", id_producto)

    def update_summary(self, total_ventas, total_pedidos, top_producto, top_cliente):
        self.label_total_ventas.setText(f"Ventas Totales: ${total_ventas:.2f}")
        self.label_total_pedidos.setText(f"Total Pedidos: {total_pedidos}")
        self.label_producto_top.setText(f"Producto más vendido: {top_producto}")
        self.label_cliente_top.setText(f"Cliente top: {top_cliente}")

    def update_table(self, data):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            self.model.appendRow(items)

    def update_graphs(self, sales_data, client_data, best_products, worst_products):
        self.axes.clear()
        plt.style.use('dark_background')
        for ax in self.axes.flat:
            ax.set_facecolor('#4d5a62')
            ax.tick_params(colors='#969fa3')
            ax.spines['top'].set_color('#676d71')
            ax.spines['right'].set_color('#676d71')
            ax.spines['left'].set_color('#676d71')
            ax.spines['bottom'].set_color('#676d71')

        # Ventas Totales
        dates = [row[0] for row in sales_data]
        totals = [row[1] for row in sales_data]
        self.axes[0, 0].bar(dates, totals, color='#676d71')
        self.axes[0, 0].set_title("Ventas Totales", color='#969a9a')
        self.axes[0, 0].tick_params(axis='x', rotation=45)

        # Top Clientes
        clients = [row[0][:10] for row in client_data]
        client_totals = [row[1] for row in client_data]
        self.axes[0, 1].bar(clients, client_totals, color='#676d71')
        self.axes[0, 1].set_title("Mejores Clientes", color='#969a9a')
        self.axes[0, 1].tick_params(axis='x', rotation=45)

        # Productos Más Vendidos
        products = [row[0][:10] for row in best_products]
        quantities = [row[1] for row in best_products]
        self.axes[1, 0].bar(products, quantities, color='#676d71')
        self.axes[1, 0].set_title("Productos Más Vendidos", color='#969a9a')
        self.axes[1, 0].tick_params(axis='x', rotation=45)

        # Productos Menos Vendidos
        products = [row[0][:10] for row in worst_products]
        quantities = [row[1] for row in worst_products]
        self.axes[1, 1].bar(products, quantities, color='#676d71')
        self.axes[1, 1].set_title("Productos Menos Vendidos", color='#969a9a')
        self.axes[1, 1].tick_params(axis='x', rotation=45)

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_filters(self):
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_fin.setDate(QDate.currentDate())
        self.cliente_cb.setCurrentIndex(0)
        self.producto_cb.setCurrentIndex(0)
        self.period_cb.setCurrentIndex(0)

    def get_filter_values(self):
        return {
            'start_date': self.fecha_inicio.date().toString("yyyy-MM-dd"),
            'end_date': self.fecha_fin.date().toString("yyyy-MM-dd"),
            'cliente_id': self.cliente_cb.currentData(),
            'producto_id': self.producto_cb.currentData(),
            'period': self.period_cb.currentText()
        }

    def set_start_date(self, start_date):
        self.fecha_inicio.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))