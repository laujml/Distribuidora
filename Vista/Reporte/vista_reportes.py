from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QFileDialog,
    QScrollArea, QFrame, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Styles import Styles

class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportes de Ventas")
        
        # Obtener información de la pantalla para hacer responsive
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        
        # Establecer tamaño mínimo basado en la pantalla
        min_width = min(1000, int(self.screen_width * 0.8))
        min_height = min(800, int(self.screen_height * 0.8))
        self.setMinimumSize(min_width, min_height)
        
        # Configurar políticas de tamaño para que sea responsive
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz de usuario para la vista de reportes.
        """
        # Layout principal con scroll para pantallas pequeñas
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Área de scroll para contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget contenedor para el scroll
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Título - Responsive font size
        self.titulo = QLabel("Reporte de Ventas")
        title_font_size = max(14, min(18, int(self.screen_width / 80)))
        self.titulo.setFont(QFont("Arial", title_font_size, QFont.Weight.Bold))
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Styles.apply_styles(self.titulo)
        layout.addWidget(self.titulo)

        # Filtros - Layout responsive
        self.create_filters_section(layout)

        # Resumen - Layout responsive
        self.create_summary_section(layout)

        # Gráficos - Tamaño más grande (sin tabla visible)
        self.create_charts_section(layout)

        # Tabla oculta - solo para exportación
        self.create_table_section(layout)

        # Botones - Layout responsive
        self.create_buttons_section(layout)

        # Configurar scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_filters_section(self, layout):
        """Crea la sección de filtros con layout responsive"""
        filtros_frame = QFrame()
        filtros_frame.setFrameStyle(QFrame.Shape.Box)
        filtros_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Layout adaptable para filtros
        if self.screen_width < 1200:
            # Para pantallas pequeñas, usar layout vertical
            filtros_layout = QVBoxLayout()
            
            # Primera fila
            row1 = QHBoxLayout()
            row1.addWidget(QLabel("Período:"))
            self.period_cb = QComboBox()
            self.period_cb.addItems(["Semanal", "Mensual"])
            self.period_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.period_cb)
            row1.addWidget(self.period_cb)
            
            row1.addWidget(QLabel("Desde:"))
            self.fecha_inicio = QDateEdit()
            self.fecha_inicio.setCalendarPopup(True)
            self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
            self.fecha_inicio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.fecha_inicio)
            row1.addWidget(self.fecha_inicio)
            
            row1.addWidget(QLabel("Hasta:"))
            self.fecha_fin = QDateEdit()
            self.fecha_fin.setCalendarPopup(True)
            self.fecha_fin.setDate(QDate.currentDate())
            self.fecha_fin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.fecha_fin)
            row1.addWidget(self.fecha_fin)
            
            # Segunda fila
            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Cliente:"))
            self.cliente_cb = QComboBox()
            self.cliente_cb.addItem("Todos los clientes")
            self.cliente_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.cliente_cb)
            row2.addWidget(self.cliente_cb)
            
            row2.addWidget(QLabel("Producto:"))
            self.producto_cb = QComboBox()
            self.producto_cb.addItem("Todos los productos")
            self.producto_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.producto_cb)
            row2.addWidget(self.producto_cb)
            
            # Tercera fila - Botones
            row3 = QHBoxLayout()
            self.buscar_btn = QPushButton("Buscar")
            self.buscar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.buscar_btn)
            row3.addWidget(self.buscar_btn)
            
            self.limpiar_btn = QPushButton("Limpiar filtros")
            self.limpiar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.limpiar_btn)
            row3.addWidget(self.limpiar_btn)
            
            filtros_layout.addLayout(row1)
            filtros_layout.addLayout(row2)
            filtros_layout.addLayout(row3)
            
        else:
            # Para pantallas grandes, usar layout horizontal
            filtros_layout = QHBoxLayout()
            
            # Añadir todos los controles en una sola fila
            controls = [
                ("Período:", self.create_period_combo()),
                ("Desde:", self.create_start_date()),
                ("Hasta:", self.create_end_date()),
                ("Cliente:", self.create_client_combo()),
                ("Producto:", self.create_product_combo())
            ]
            
            for label_text, control in controls:
                label = QLabel(label_text)
                Styles.apply_styles(label)
                filtros_layout.addWidget(label)
                filtros_layout.addWidget(control)
            
            # Botones
            self.buscar_btn = QPushButton("Buscar")
            self.buscar_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.buscar_btn)
            filtros_layout.addWidget(self.buscar_btn)
            
            self.limpiar_btn = QPushButton("Limpiar filtros")
            self.limpiar_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            Styles.apply_styles(self.limpiar_btn)
            filtros_layout.addWidget(self.limpiar_btn)
        
        # Aplicar estilos a los labels
        for i in range(filtros_layout.count()):
            item = filtros_layout.itemAt(i)
            if item and hasattr(item, 'widget') and isinstance(item.widget(), QLabel):
                Styles.apply_styles(item.widget())
        
        filtros_frame.setLayout(filtros_layout)
        layout.addWidget(filtros_frame)

    def create_period_combo(self):
        self.period_cb = QComboBox()
        self.period_cb.addItems(["Semanal", "Mensual"])
        self.period_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.period_cb)
        return self.period_cb

    def create_start_date(self):
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_inicio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.fecha_inicio)
        return self.fecha_inicio

    def create_end_date(self):
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.fecha_fin)
        return self.fecha_fin

    def create_client_combo(self):
        self.cliente_cb = QComboBox()
        self.cliente_cb.addItem("Todos los clientes")
        self.cliente_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.cliente_cb)
        return self.cliente_cb

    def create_product_combo(self):
        self.producto_cb = QComboBox()
        self.producto_cb.addItem("Todos los productos")
        self.producto_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.producto_cb)
        return self.producto_cb

    def create_summary_section(self, layout):
        """Crea la sección de resumen con layout responsive"""
        resumen_frame = QFrame()
        resumen_frame.setFrameStyle(QFrame.Shape.Box)
        resumen_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Layout adaptable para resumen
        if self.screen_width < 800:
            # Para pantallas muy pequeñas, usar layout vertical
            resumen_layout = QVBoxLayout()
        else:
            # Para pantallas normales, usar layout horizontal
            resumen_layout = QHBoxLayout()
        
        # Crear labels del resumen
        self.label_total_ventas = QLabel("Ventas Totales: $0.00")
        self.label_total_ventas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.label_total_ventas)
        
        self.label_total_pedidos = QLabel("Total Pedidos: 0")
        self.label_total_pedidos.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.label_total_pedidos)
        
        self.label_producto_top = QLabel("Producto más vendido: -")
        self.label_producto_top.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.label_producto_top)
        
        self.label_cliente_top = QLabel("Cliente top: -")
        self.label_cliente_top.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.label_cliente_top)
        
        resumen_layout.addWidget(self.label_total_ventas)
        resumen_layout.addWidget(self.label_total_pedidos)
        resumen_layout.addWidget(self.label_producto_top)
        resumen_layout.addWidget(self.label_cliente_top)
        
        resumen_frame.setLayout(resumen_layout)
        layout.addWidget(resumen_frame)

    def create_charts_section(self, layout):
        """Crea la sección de gráficos con tamaño más grande (sin tabla visible)"""
        # Calcular tamaño de figura más grande ya que no hay tabla
        fig_width = max(12, min(20, self.screen_width / 80))
        fig_height = max(10, min(16, self.screen_height / 80))
        
        # Configurar matplotlib para mejor visualización
        plt.rcParams.update({
            'font.size': max(10, min(14, int(self.screen_width / 100))),
            'axes.titlesize': max(12, min(16, int(self.screen_width / 80))),
            'axes.labelsize': max(10, min(14, int(self.screen_width / 100))),
            'xtick.labelsize': max(8, min(12, int(self.screen_width / 120))),
            'ytick.labelsize': max(8, min(12, int(self.screen_width / 120)))
        })
        
        self.figure, self.axes = plt.subplots(2, 2, figsize=(fig_width, fig_height))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Configurar altura más grande para los gráficos (sin tabla)
        min_chart_height = max(500, int(self.screen_height * 0.5))
        max_chart_height = max(800, int(self.screen_height * 0.7))
        self.canvas.setMinimumHeight(min_chart_height)
        self.canvas.setMaximumHeight(max_chart_height)
        
        layout.addWidget(self.canvas)

    def create_table_section(self, layout):
        """Crea la tabla (oculta) solo para funcionalidad de exportación"""
        # Tabla oculta - solo para exportación a Excel
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        self.tabla.setVisible(False)  # Ocultar la tabla
        
        # Configurar el redimensionamiento de columnas
        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        
        Styles.apply_styles(self.tabla)
        # No agregar al layout para que no sea visible

    def create_buttons_section(self, layout):
        """Crea la sección de botones responsive"""
        botones_layout = QHBoxLayout()
        
        self.btn_exportar = QPushButton("Exportar a Excel")
        self.btn_exportar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.btn_exportar)
        
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        Styles.apply_styles(self.btn_actualizar)
        
        botones_layout.addWidget(self.btn_exportar)
        botones_layout.addWidget(self.btn_actualizar)
        layout.addLayout(botones_layout)

    def resizeEvent(self, event):
        """Maneja el evento de redimensionamiento para ajustar elementos"""
        super().resizeEvent(event)
        
        # Actualizar tamaños de fuente si es necesario
        current_width = self.width()
        title_font_size = max(14, min(18, int(current_width / 80)))
        self.titulo.setFont(QFont("Arial", title_font_size, QFont.Weight.Bold))
        
        # La tabla está oculta, no necesita redimensionamiento visual
        # pero mantiene funcionalidad para exportación
        if hasattr(self, 'tabla'):
            self.tabla.resizeColumnsToContents()

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
            self.axes[0, 0].plot(dates, totals, color='#969fa3', linewidth=2)
        self.axes[0, 0].set_title("Ventas Totales", color='#969a9a')
        self.axes[0, 0].tick_params(axis='x', rotation=45)

        # Mejores Clientes
        if client_data:
            clients, client_totals = zip(*client_data)
            # Truncar nombres largos para mejor visualización
            clients = [c[:15] + '...' if len(c) > 15 else c for c in clients]
            self.axes[0, 1].bar(clients, client_totals, color='#969a9a')
        self.axes[0, 1].set_title("Mejores Clientes", color='#969a9a')
        self.axes[0, 1].tick_params(axis='x', rotation=45)

        # Productos Más Vendidos
        if best_products:
            products, quantities = zip(*best_products)
            # Truncar nombres largos para mejor visualización
            products = [p[:20] + '...' if len(p) > 20 else p for p in products]
            self.axes[1, 0].barh(products, quantities, color='#969a9a')
        self.axes[1, 0].set_title("Productos Más Vendidos", color='#969a9a')

        # Productos Menos Vendidos
        if worst_products:
            products, quantities = zip(*worst_products)
            # Truncar nombres largos para mejor visualización
            products = [p[:20] + '...' if len(p) > 20 else p for p in products]
            self.axes[1, 1].barh(products, quantities, color='#969a9a')
        self.axes[1, 1].set_title("Productos Menos Vendidos", color='#969a9a')

        self.figure.tight_layout(pad=2.0)
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
