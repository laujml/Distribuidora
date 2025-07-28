from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QDateEdit, QMessageBox, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Modelo.ui_config import UIConfig

class ReportesView(QWidget):
    back_clicked = pyqtSignal()
    period_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        UIConfig.configure_layout(main_layout)

        self.titulo = QLabel("Reporte de Ventas")
        UIConfig.configure_label(self.titulo, is_title=True)
        main_layout.addWidget(self.titulo)

        filtros_layout = QHBoxLayout()
        UIConfig.configure_layout(filtros_layout)

        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        self.period_cb.currentTextChanged.connect(self.on_period_changed)
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

        for cb in [self.period_cb, self.fecha_inicio, self.fecha_fin, self.cliente_cb, self.producto_cb]:
            UIConfig.configure_control(cb)

        self.buscar_btn = QPushButton("Buscar")
        self.limpiar_btn = QPushButton("Limpiar filtros")
        self.back_btn = QPushButton("Regresar")

        self.back_btn.clicked.connect(self.back_clicked)

        for label_text, widget in [
            ("Período:", self.period_cb),
            ("Desde:", self.fecha_inicio),
            ("Hasta:", self.fecha_fin),
            ("Cliente:", self.cliente_cb),
            ("Producto:", self.producto_cb)
        ]:
            label = QLabel(label_text)
            UIConfig.configure_label(label)
            filtros_layout.addWidget(label)
            filtros_layout.addWidget(widget)

        filtros_layout.addWidget(self.buscar_btn)
        filtros_layout.addWidget(self.limpiar_btn)
        filtros_layout.addWidget(self.back_btn)
        main_layout.addLayout(filtros_layout)

        resumen_layout = QHBoxLayout()
        UIConfig.configure_layout(resumen_layout)

        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        self.label_producto_top = QLabel("Producto más vendido: -")
        self.label_cliente_top = QLabel("Cliente top: -")

        for label in [self.label_total_ventas, self.label_total_pedidos, self.label_producto_top, self.label_cliente_top]:
            UIConfig.configure_label(label)
            resumen_layout.addWidget(label)

        main_layout.addLayout(resumen_layout)

        self.figure = Figure(figsize=(12, 8), tight_layout=True)
        self.axes = self.figure.subplots(2, 2)
        self.canvas = FigureCanvas(self.figure)
        UIConfig.configure_canvas(self.canvas)
        main_layout.addWidget(self.canvas)

        botones_layout = QHBoxLayout()
        UIConfig.configure_layout(botones_layout)
        self.btn_exportar = QPushButton("Exportar a Excel")
        self.btn_actualizar = QPushButton("Actualizar")
        for btn in [self.btn_exportar, self.btn_actualizar]:
            botones_layout.addWidget(btn)
        main_layout.addLayout(botones_layout)

        main_layout.addStretch()

        contenido_widget = QWidget()
        contenido_widget.setLayout(main_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(contenido_widget)

        layout_final = QVBoxLayout()
        layout_final.addWidget(scroll_area)
        self.setLayout(layout_final)

    def set_periodo(self, periodo):
        self.period_cb.setCurrentText(periodo)
        self.titulo.setText(f"Reporte {periodo}")
        print(f"Title updated to: Reporte {periodo}")
        end_date = self.fecha_fin.date()
        if periodo == "Semanal":
            self.fecha_inicio.setDate(end_date.addDays(-6))
        else:
            self.fecha_inicio.setDate(end_date.addMonths(-1))

    def on_period_changed(self, periodo):
        self.set_periodo(periodo)
        self.period_changed.emit(periodo)

    def populate_clientes(self, clientes):
        self.cliente_cb.clear()
        self.cliente_cb.addItem("Todos los clientes")
        for id_cliente, nombre in clientes:
            self.cliente_cb.addItem(f"{id_cliente} - {nombre}", id_cliente)

    def populate_productos(self, productos):
        self.producto_cb.clear()
        self.producto_cb.addItem("Todos los productos")
        for id_producto, desc in productos:
            self.producto_cb.addItem(f"{id_producto} - {desc}", id_producto)

    def update_summary(self, total_ventas, total_pedidos, top_producto, top_cliente):
        self.label_total_ventas.setText(f"Ventas Totales: ${total_ventas:.2f}")
        self.label_total_pedidos.setText(f"Total Pedidos: {total_pedidos}")
        self.label_producto_top.setText(f"Producto más vendido: {top_producto}")
        self.label_cliente_top.setText(f"Cliente top: {top_cliente}")

    def update_graphs(self, sales_data, client_data, best_products, worst_products):
        for ax in self.axes.flat:
            ax.clear()
        if sales_data:
            dates, totals = zip(*sales_data)
            self.axes[0, 0].plot(dates, totals)
        self.axes[0, 0].set_title("Ventas Totales")
        self.axes[0, 0].tick_params(axis='x', rotation=45)
        if client_data:
            clients, client_totals = zip(*client_data)
            self.axes[0, 1].bar(clients, client_totals)
        self.axes[0, 1].set_title("Mejores Clientes")
        self.axes[0, 1].tick_params(axis='x', rotation=45)
        if best_products:
            products, quantities = zip(*best_products)
            self.axes[1, 0].barh(products, quantities)
        self.axes[1, 0].set_title("Productos Más Vendidos")
        if worst_products:
            products, quantities = zip(*worst_products)
            self.axes[1, 1].barh(products, quantities)
        self.axes[1, 1].set_title("Productos Menos Vendidos")
        self.figure.tight_layout()
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

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Información", message)

    def get_export_path(self):
        return QFileDialog.getSaveFileName(self, "Guardar Reporte", "reporte_ventas.xlsx", "Excel Files (*.xlsx)")[0]
