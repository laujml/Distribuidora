from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QFileDialog,
    QSizePolicy, QScrollArea, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ReportesView(QWidget):
    period_changed = pyqtSignal(str)
    regresar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(20)

        self.titulo = QLabel("Reporte Mensual")
        self.titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            QLabel {
                color: #f0f0f0;
                background-color: transparent;
                padding: 20px;
            }
        """)
        layout_principal.addWidget(self.titulo)

        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        self.period_cb.currentTextChanged.connect(self.period_changed.emit)
        self.period_cb.hide()

        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_inicio.hide()

        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.hide()

        self.cliente_cb = QComboBox()
        self.cliente_cb.addItem("Todos los clientes")
        self.cliente_cb.hide()

        self.producto_cb = QComboBox()
        self.producto_cb.addItem("Todos los productos")
        self.producto_cb.hide()

        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.hide()
        self.limpiar_btn = QPushButton("Limpiar filtros")
        self.limpiar_btn.hide()

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(15)

        self.label_fechas = QLabel()
        self.label_fechas.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                color: #4d5a62;
                border: none;
                border-radius: 25px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.actualizar_label_fechas()

        self.btn_calendario = QPushButton("📅")
        self.btn_calendario.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #4d5a62;
                border: none;
                border-radius: 25px;
                padding: 12px 16px;
                font-size: 16px;
                font-weight: bold;
                min-width: 50px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        filtros_layout.addStretch()
        filtros_layout.addWidget(self.label_fechas)
        filtros_layout.addWidget(self.btn_calendario)
        filtros_layout.addStretch()

        layout_principal.addLayout(filtros_layout)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        self.card_venta_total = self.create_card()
        self.card_clientes = self.create_card()
        self.card_productos_mas = self.create_card()
        self.card_productos_menos = self.create_card()

        self.setup_card_venta_total()
        self.setup_grafico_clientes()
        self.setup_grafico_productos_mas()
        self.setup_grafico_productos_menos()

        cards_layout.addWidget(self.card_venta_total, 0, 0)
        cards_layout.addWidget(self.card_clientes, 0, 1)
        cards_layout.addWidget(self.card_productos_mas, 1, 0)
        cards_layout.addWidget(self.card_productos_menos, 1, 1)

        cards_layout.setRowStretch(0, 1)
        cards_layout.setRowStretch(1, 1)
        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)

        layout_principal.addLayout(cards_layout, 1)

        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        self.label_producto_top = QLabel("Producto más vendido: -")
        self.label_cliente_top = QLabel("Cliente top: -")
        for label in [self.label_total_ventas, self.label_total_pedidos, self.label_producto_top, self.label_cliente_top]:
            label.hide()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.horizontalHeader().setVisible(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.hide()

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        self.btn_exportar = QPushButton("Exportar a Excel")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_clicked.emit)

        button_style = """
            QPushButton {
                background-color: #676d71;
                color: #f0f0f0;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4d5a62;
            }
        """

        for btn in [self.btn_exportar, self.btn_actualizar, self.btn_regresar]:
            btn.setStyleSheet(button_style)
            botones_layout.addWidget(btn)

        botones_layout.addStretch()
        layout_principal.addLayout(botones_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        contenido_widget = QWidget()
        contenido_widget.setLayout(layout_principal)
        scroll_area.setWidget(contenido_widget)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #4d5a62; }")

        layout_final = QVBoxLayout()
        layout_final.setContentsMargins(0, 0, 0, 0)
        layout_final.addWidget(scroll_area)
        self.setLayout(layout_final)

        self.setStyleSheet("""
            QWidget {
                background-color: #4d5a62;
            }
        """)

    def create_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card.setMinimumSize(300, 250)
        return card

    def setup_card_venta_total(self):
        layout = QVBoxLayout()
        self.label_venta_total = QLabel("Venta Total")
        self.label_venta_total.setStyleSheet("""
            font-size: 18px; 
            color: #4d5a62; 
            margin-bottom: 15px; 
            font-weight: bold;
        """)
        self.label_venta_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.valor_venta_total = QLabel("$1,000.00")
        self.valor_venta_total.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #4d5a62;
        """)
        self.valor_venta_total.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label_venta_total)
        layout.addWidget(self.valor_venta_total)
        layout.addStretch()

        self.card_venta_total.setLayout(layout)
        self.card_venta_total.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 3px solid #9c27b0;
                border-radius: 15px;
                padding: 20px;
            }
        """)

    def setup_grafico_clientes(self):
        layout = QVBoxLayout()
        titulo = QLabel("Mejores Clientes")
        titulo.setStyleSheet("""
            font-size: 16px; 
            color: #4d5a62; 
            font-weight: bold; 
            margin-bottom: 10px;
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.figure_clientes = Figure(figsize=(4, 3), tight_layout=True)
        self.ax_clientes = self.figure_clientes.add_subplot(111)
        self.canvas_clientes = FigureCanvas(self.figure_clientes)
        self.canvas_clientes.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas_clientes, 1)
        self.card_clientes.setLayout(layout)

    def setup_grafico_productos_mas(self):
        layout = QVBoxLayout()
        titulo = QLabel("Productos Más Vendidos")
        titulo.setStyleSheet("""
            font-size: 16px; 
            color: #4d5a62; 
            font-weight: bold; 
            margin-bottom: 10px;
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.figure_productos_mas = Figure(figsize=(4, 3), tight_layout=True)
        self.ax_productos_mas = self.figure_productos_mas.add_subplot(111)
        self.canvas_productos_mas = FigureCanvas(self.figure_productos_mas)
        self.canvas_productos_mas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas_productos_mas, 1)
        self.card_productos_mas.setLayout(layout)

    def setup_grafico_productos_menos(self):
        layout = QVBoxLayout()
        titulo = QLabel("Productos Menos Vendidos")
        titulo.setStyleSheet("""
            font-size: 16px; 
            color: #4d5a62; 
            font-weight: bold; 
            margin-bottom: 10px;
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.figure_productos_menos = Figure(figsize=(4, 3), tight_layout=True)
        self.ax_productos_menos = self.figure_productos_menos.add_subplot(111)
        self.canvas_productos_menos = FigureCanvas(self.figure_productos_menos)
        self.canvas_productos_menos.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas_productos_menos, 1)
        self.card_productos_menos.setLayout(layout)

    def actualizar_label_fechas(self):
        fecha_inicio = self.fecha_inicio.date().toString("dd/MM/yyyy")
        fecha_fin = self.fecha_fin.date().toString("dd/MM/yyyy")
        self.label_fechas.setText(f"{fecha_inicio} - {fecha_fin}")

    def set_periodo(self, periodo):
        self.period_cb.blockSignals(True)
        self.period_cb.setCurrentText(periodo)
        self.titulo.setText(f"Reporte {periodo}")
        self.period_cb.blockSignals(False)

    def set_start_date(self, start_date):
        self.fecha_inicio.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))

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
        self.valor_venta_total.setText(f"${total_ventas:,.2f}")
        self.label_total_ventas.setText(f"Ventas Totales: ${total_ventas:.2f}")
        self.label_total_pedidos.setText(f"Total Pedidos: {total_pedidos}")
        self.label_producto_top.setText(f"Producto más vendido: {top_producto}")
        self.label_cliente_top.setText(f"Cliente top: {top_cliente}")

    def actualizar_tabla(self, datos):
        self.tabla.setRowCount(0)
        for row, (fecha, cliente, producto, cantidad, subtotal) in enumerate(datos):
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(row, 1, QTableWidgetItem(cliente))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(row, 4, QTableWidgetItem(f"${subtotal:.2f}"))

    def get_table_data_for_export(self):
        headers = ["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"]
        data = [headers]
        for row in range(self.tabla.rowCount()):
            row_data = []
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return data

    def update_graphs(self, sales_data, client_data, best_products, worst_products):
        self.ax_clientes.clear()
        self.ax_productos_mas.clear()
        self.ax_productos_menos.clear()

        for ax in [self.ax_clientes, self.ax_productos_mas, self.ax_productos_menos]:
            ax.set_facecolor('#ffffff')
            ax.tick_params(colors='#4d5a62', labelsize=8)
            for spine in ax.spines.values():
                spine.set_color('#dee2e6')

        if client_data:
            clients, client_totals = zip(*client_data)
            bars = self.ax_clientes.barh(clients, client_totals, color='#4d5a62', alpha=0.8)
            self.ax_clientes.set_xlim(0, max(client_totals) * 1.1)
            for bar, value in zip(bars, client_totals):
                width = bar.get_width()
                self.ax_clientes.text(width + max(client_totals) * 0.02,
                                     bar.get_y() + bar.get_height()/2.,
                                     f'${value:.0f}', ha='left', va='center',
                                     fontsize=7, color='#4d5a62', fontweight='bold')
        self.ax_clientes.grid(True, alpha=0.3, axis='x')

        if best_products:
            products, quantities = zip(*best_products)
            bars = self.ax_productos_mas.bar(range(len(products)), quantities,
                                           color='#4d5a62', alpha=0.8)
            self.ax_productos_mas.set_xticks([])
            self.ax_productos_mas.set_ylim(0, max(quantities) * 1.1)
            for bar, value in zip(bars, quantities):
                height = bar.get_height()
                self.ax_productos_mas.text(bar.get_x() + bar.get_width()/2.,
                                         height + max(quantities) * 0.02,
                                         f'{value}', ha='center', va='bottom',
                                         fontsize=7, color='#4d5a62', fontweight='bold')
        self.ax_productos_mas.grid(True, alpha=0.3, axis='y')

        if worst_products:
            products, quantities = zip(*worst_products)
            bars = self.ax_productos_menos.bar(range(len(products)), quantities,
                                             color='#676d71', alpha=0.8)
            self.ax_productos_menos.set_xticks([])
            self.ax_productos_menos.set_ylim(0, max(quantities) * 1.1)
            for bar, value in zip(bars, quantities):
                height = bar.get_height()
                self.ax_productos_menos.text(bar.get_x() + bar.get_width()/2.,
                                           height + max(quantities) * 0.02,
                                           f'{value}', ha='center', va='bottom',
                                           fontsize=7, color='#4d5a62', fontweight='bold')
        self.ax_productos_menos.grid(True, alpha=0.3, axis='y')

        self.figure_clientes.tight_layout(pad=0.5)
        self.figure_productos_mas.tight_layout(pad=0.5)
        self.figure_productos_menos.tight_layout(pad=0.5)

        self.canvas_clientes.draw()
        self.canvas_productos_mas.draw()
        self.canvas_productos_menos.draw()

    def reset_filters(self):
        self.cliente_cb.setCurrentIndex(0)
        self.producto_cb.setCurrentIndex(0)

    def get_filter_values(self):
        return {
            'start_date': self.fecha_inicio.date().toString("yyyy-MM-dd"),
            'end_date': self.fecha_fin.date().toString("yyyy-MM-dd"),
            'cliente_id': self.cliente_cb.currentData(),
            'producto_id': self.producto_cb.currentData(),
            'period': self.period_cb.currentText()
        }

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Información", message)

    def get_export_path(self):
        return QFileDialog.getSaveFileName(self, "Guardar Reporte", "reporte_ventas.xlsx", "Excel Files (*.xlsx)")[0]
