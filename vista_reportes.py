from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from recursos.Styles import Styles

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        self.setMinimumSize(1000, 800)
        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz de usuario para la vista de reportes.
        """
        layout = QVBoxLayout()

        # Título
        self.titulo = QLabel("Reporte de Ventas")
        self.titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        Styles.apply_styles(self.titulo)
        layout.addWidget(self.titulo)

        # Filtros
        filtros_layout = QHBoxLayout()
        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        Styles.apply_styles(self.period_cb)
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        Styles.apply_styles(self.fecha_inicio)
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        Styles.apply_styles(self.fecha_fin)
        self.cliente_cb = QComboBox()
        self.cliente_cb.addItem("Todos los clientes")
        Styles.apply_styles(self.cliente_cb)
        self.producto_cb = QComboBox()
        self.producto_cb.addItem("Todos los productos")
        Styles.apply_styles(self.producto_cb)
        self.buscar_btn = QPushButton("Buscar")
        Styles.apply_styles(self.buscar_btn)
        self.limpiar_btn = QPushButton("Limpiar filtros")
        Styles.apply_styles(self.limpiar_btn)

        filtros_layout.addWidget(QLabel("Período:"))
        Styles.apply_styles(filtros_layout.itemAt(filtros_layout.count()-1).widget())
        filtros_layout.addWidget(self.period_cb)
        filtros_layout.addWidget(QLabel("Desde:"))
        Styles.apply_styles(filtros_layout.itemAt(filtros_layout.count()-1).widget())
        filtros_layout.addWidget(self.fecha_inicio)
        filtros_layout.addWidget(QLabel("Hasta:"))
        Styles.apply_styles(filtros_layout.itemAt(filtros_layout.count()-1).widget())
        filtros_layout.addWidget(self.fecha_fin)
        filtros_layout.addWidget(QLabel("Cliente:"))
        Styles.apply_styles(filtros_layout.itemAt(filtros_layout.count()-1).widget())
        filtros_layout.addWidget(self.cliente_cb)
        filtros_layout.addWidget(QLabel("Producto:"))
        Styles.apply_styles(filtros_layout.itemAt(filtros_layout.count()-1).widget())
        filtros_layout.addWidget(self.producto_cb)
        filtros_layout.addWidget(self.buscar_btn)
        filtros_layout.addWidget(self.limpiar_btn)
        layout.addLayout(filtros_layout)

        # Resumen
        resumen_layout = QHBoxLayout()
        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        Styles.apply_styles(self.label_total_ventas)
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        Styles.apply_styles(self.label_total_pedidos)
        self.label_producto_top = QLabel("Producto más vendido: -")
        Styles.apply_styles(self.label_producto_top)
        self.label_cliente_top = QLabel("Cliente top: -")
        Styles.apply_styles(self.label_cliente_top)
        resumen_layout.addWidget(self.label_total_ventas)
        resumen_layout.addWidget(self.label_total_pedidos)
        resumen_layout.addWidget(self.label_producto_top)
        resumen_layout.addWidget(self.label_cliente_top)
        layout.addLayout(resumen_layout)

        # Gráficos
        self.figure, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        Styles.apply_styles(self.tabla)
        layout.addWidget(self.tabla)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_exportar = QPushButton("Exportar a Excel")
        Styles.apply_styles(self.btn_exportar)
        self.btn_actualizar = QPushButton("Actualizar")
        Styles.apply_styles(self.btn_actualizar)
        botones_layout.addWidget(self.btn_exportar)
        botones_layout.addWidget(self.btn_actualizar)
        layout.addLayout(botones_layout)

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
        """
        Pobla el combo box de productos con la lista de productos.

        Args:
            productos (list): Lista de tuplas con el ID y descripción de cada producto.
        """
        self.producto_cb.clear()
        self.producto_cb.addItem("Todos los productos")
        for id_producto, desc in productos:
            self.producto_cb.addItem(f"{id_producto} - {desc}", id_producto)

    def update_summary(self, total_ventas, total_pedidos, top_producto, top_cliente):
        """
        Actualiza los labels del resumen con los datos proporcionados.

        Args:
            total_ventas (float): Total de ventas.
            total_pedidos (int): Total de pedidos.
            top_producto (str): Producto más vendido.
            top_cliente (str): Cliente top.
        """
        self.label_total_ventas.setText(f"Ventas Totales: ${total_ventas:.2f}")
        self.label_total_pedidos.setText(f"Total Pedidos: {total_pedidos}")
        self.label_producto_top.setText(f"Producto más vendido: {top_producto}")
        self.label_cliente_top.setText(f"Cliente top: {top_cliente}")

    def actualizar_tabla(self, datos):
        """
        Actualiza la tabla con el detalle de las ventas.

        Args:
            datos (list): Lista de tuplas con la fecha, cliente, producto, cantidad y subtotal de cada venta.
        """
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
        """
        Actualiza los gráficos con los datos proporcionados.

        Args:
            sales_data (list): Lista de tuplas con la fecha y el total de ventas.
            client_data (list): Lista de tuplas con el nombre del cliente y el total de ventas.
            best_products (list): Lista de tuplas con la descripción del producto y la cantidad vendida (mejores).
            worst_products (list): Lista de tuplas con la descripción del producto y la cantidad vendida (peores).
        """
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
        """
        Restablece los filtros a sus valores predeterminados.
        """
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_fin.setDate(QDate.currentDate())
        self.cliente_cb.setCurrentIndex(0)
        self.producto_cb.setCurrentIndex(0)
        self.period_cb.setCurrentIndex(0)

    def get_filter_values(self):
        """
        Obtiene los valores actuales de los filtros.

        Returns:
            Un diccionario con los valores de los filtros.
        """
        return {
            'start_date': self.fecha_inicio.date().toString("yyyy-MM-dd"),
            'end_date': self.fecha_fin.date().toString("yyyy-MM-dd"),
            'cliente_id': self.cliente_cb.currentData(),
            'producto_id': self.producto_cb.currentData(),
            'period': self.period_cb.currentText()
        }

    def set_start_date(self, start_date):
        """
        Establece la fecha de inicio del rango.

        Args:
            start_date (str): Fecha de inicio del rango.
        """
        self.fecha_inicio.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))

    def show_error(self, message):
        """
        Muestra un mensaje de error.

        Args:
            message (str): Mensaje de error.
        """
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        """
        Muestra un mensaje de información.

        Args:
            message (str): Mensaje de información.
        """
        QMessageBox.information(self, "Información", message)

    def get_export_path(self):
        """
        Obtiene la ruta del archivo para exportar a Excel.

        Returns:
            La ruta del archivo seleccionado.
        """
        return QFileDialog.getSaveFileName(self, "Guardar Reporte", "reporte_ventas.xlsx", "Excel Files (*.xlsx)")[0]
