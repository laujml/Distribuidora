from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QFileDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        self.setMinimumSize(1000, 800)  
        self.init_ui()

    def init_ui(self):
        
        layout = QVBoxLayout()

        
        self.titulo = QLabel("Reporte de Ventas")
        self.titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            QLabel {
                color: #969a9a;
                background-color: #4d5a62;
                padding: 10px;
            }
        """)
        layout.addWidget(self.titulo)

       
        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        self.period_cb.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.period_cb.setStyleSheet("""
            QComboBox {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #676d71;
                color: #969fa3;
                selection-background-color: #4d5a62;
            }
        """)
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_inicio.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.fecha_inicio.setStyleSheet("""
            QDateEdit {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                padding: 5px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """)
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.fecha_fin.setStyleSheet("""
            QDateEdit {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                padding: 5px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """)
        self.cliente_cb = QComboBox()
        self.cliente_cb.addItem("Todos los clientes")
        self.cliente_cb.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.cliente_cb.setStyleSheet("""
            QComboBox {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #676d71;
                color: #969fa3;
                selection-background-color: #4d5a62;
            }
        """)
        self.producto_cb = QComboBox()
        self.producto_cb.addItem("Todos los productos")
        self.producto_cb.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.producto_cb.setStyleSheet("""
            QComboBox {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #676d71;
                color: #969fa3;
                selection-background-color: #4d5a62;
            }
        """)
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setStyleSheet("""
            QPushButton {
                background-color: #40464b;
                color: #969fa3;
                border: 1px solid #1d222e;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4d5a62;
            }
        """)
        self.limpiar_btn = QPushButton("Limpiar filtros")
        self.limpiar_btn.setStyleSheet("""
            QPushButton {
                background-color: #40464b;
                color: #969fa3;
                border: 1px solid #1d222e;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4d5a62;
            }
        """)

        for label_text, widget in [
            ("Período:", self.period_cb),
            ("Desde:", self.fecha_inicio),
            ("Hasta:", self.fecha_fin),
            ("Cliente:", self.cliente_cb),
            ("Producto:", self.producto_cb)
        ]:
            label = QLabel(label_text)
            label.setStyleSheet("""
                QLabel {
                    color: #969fa3;
                    background-color: #4d5a62;
                    padding: 5px;
                }
            """)
            filtros_layout.addWidget(label)
            filtros_layout.addWidget(widget)

        filtros_layout.addWidget(self.buscar_btn)
        filtros_layout.addWidget(self.limpiar_btn)
        layout.addLayout(filtros_layout)

        resumen_layout = QHBoxLayout()
        resumen_layout.setSpacing(10)
        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        self.label_producto_top = QLabel("Producto más vendido: -")
        self.label_cliente_top = QLabel("Cliente top: -")
        for label in [self.label_total_ventas, self.label_total_pedidos, self.label_producto_top, self.label_cliente_top]:
            label.setStyleSheet("""
                QLabel {
                    color: #969fa3;
                    background-color: #4d5a62;
                    padding: 5px;
                }
            """)
            label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            resumen_layout.addWidget(label)
        layout.addLayout(resumen_layout)

        # Gráficos
        self.figure, self.axes = plt.subplots(2, 2, figsize=(12, 8))  
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.canvas)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        self.tabla.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #676d71;
                color: #969fa3;
                border: 1px solid #40464b;
                gridline-color: #1d222e;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4d5a62;
                color: #969fa3;
                padding: 5px;
                border: 1px solid #40464b;
            }
        """)
        layout.addWidget(self.tabla)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_exportar = QPushButton("Exportar a Excel")
        self.btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #40464b;
                color: #969fa3;
                border: 1px solid #1d222e;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4d5a62;
            }
        """)
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #40464b;
                color: #969fa3;
                border: 1px solid #1d222e;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4d5a62;
            }
        """)
        botones_layout.addWidget(self.btn_exportar)
        botones_layout.addWidget(self.btn_actualizar)
        layout.addLayout(botones_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #1d222e;
            }
        """)
        layout.addStretch()
        self.setLayout(layout)

    def set_periodo(self, periodo):
        """
        Establece el período seleccionado y actualiza el título.

        Args:
            periodo (str): Período seleccionado ("Semanal" o "Mensual").
        """
        self.period_cb.setCurrentText(periodo)
        self.titulo.setText(f"Reporte {periodo}")

    def populate_clientes(self, clientes):
        """
        Pobla el combo box de clientes con la lista de clientes.

        Args:
            clientes (list): Lista de tuplas con el ID y nombre de cada cliente.
        """
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

    def actualizar_tabla(self, datos):
       
        self.tabla.setRowCount(0)
        for row, (fecha, cliente, producto, cantidad, subtotal) in enumerate(datos):
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(row, 1, QTableWidgetItem(cliente))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(row, 4, QTableWidgetItem(f"${subtotal:.2f}"))
        self.tabla.resizeColumnsToContents()

    def update_graphs(self, sales_data, client_data, best_products, worst_products):
       
        for ax in self.axes.flat:
            ax.clear()
            ax.set_facecolor('#4d5a62')
            ax.tick_params(colors='#969fa3')
            for spine in ax.spines.values():
                spine.set_color('#676d71')

        # Ventas Totales
        if sales_data:
            dates, totals = zip(*sales_data)
            self.axes[0, 0].plot(dates, totals, color='#969fa3')
        self.axes[0, 0].set_title("Ventas Totales", color='#969a9a')
        self.axes[0, 0].tick_params(axis='x', rotation=45)

        # Mejores Clientes
        if client_data:
            clients, client_totals = zip(*client_data)
            self.axes[0, 1].bar(clients, client_totals, color='#969a9a')
        self.axes[0, 1].set_title("Mejores Clientes", color='#969a9a')
        self.axes[0, 1].tick_params(axis='x', rotation=45)

        # Productos Más Vendidos
        if best_products:
            products, quantities = zip(*best_products)
            self.axes[1, 0].barh(products, quantities, color='#969a9a')
        self.axes[1, 0].set_title("Productos Más Vendidos", color='#969a9a')

        # Productos Menos Vendidos
        if worst_products:
            products, quantities = zip(*worst_products)
            self.axes[1, 1].barh(products, quantities, color='#969a9a')
        self.axes[1, 1].set_title("Productos Menos Vendidos", color='#969a9a')

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

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  
    app = QApplication(sys.argv)
    window = ReportesView()
    window.show()
    sys.exit(app.exec())
