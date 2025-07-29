from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDate
from Modelomodelo_reportes import ReportesModel
from Vista.vista_reportes import ReportesView

class ReportesController:
    def __init__(self, view: ReportesView, conectar_func):
        self.view = view
        self.model = ReportesModel()
        self.stack = None
        self.setup_connections()

    def set_stack(self, stack):
        """Asignar el stack widget para poder navegar"""
        self.stack = stack

    def setup_connections(self):
        """Configurar las conexiones de los botones"""
        self.view.period_changed.connect(self.on_period_changed)
        if hasattr(self.view, 'btn_regresar'):
            self.view.btn_regresar.clicked.connect(self.regresar_a_seleccion)
        if hasattr(self.view, 'btn_actualizar'):
            self.view.btn_actualizar.clicked.connect(self.actualizar_datos)
        if hasattr(self.view, 'btn_exportar'):
            self.view.btn_exportar.clicked.connect(self.exportar_a_excel)

    def mostrar_reporte(self, periodo):
        """Mostrar reporte del período especificado"""
        self.set_periodo(periodo)
        self.actualizar_datos()

    def set_periodo(self, periodo):
        """Establecer período y fechas"""
        self.view.set_periodo(periodo)
        fecha_actual = QDate.currentDate()
        end_date = fecha_actual.toString("yyyy-MM-dd")
        start_date = self.model.adjust_date_range(end_date, periodo)
        self.view.set_start_date(start_date)
        self.view.actualizar_label_fechas()

    def on_period_changed(self, nuevo_periodo):
        """Manejar cambio de período"""
        self.set_periodo(nuevo_periodo)
        self.actualizar_datos()

    def regresar_a_seleccion(self):
        """Regresar a la pantalla de selección inicial"""
        if self.stack:
            self.stack.setCurrentIndex(0)

    def actualizar_datos(self):
        """Fetch data from model and update view"""
        try:
            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            cliente_id = filters['cliente_id']
            producto_id = filters['producto_id']

            # Obtener datos del modelo
            clientes = self.model.get_clientes()
            productos = self.model.get_productos()
            total_ventas, total_pedidos = self.model.get_total_ventas(start_date, end_date, cliente_id)
            top_cliente = self.model.get_top_cliente(start_date, end_date)
            top_producto = self.model.get_top_product(start_date, end_date)
            detalle_ventas = self.model.get_detalle_ventas(start_date, end_date, cliente_id, producto_id)
            top_clientes = self.model.get_top_clientes(start_date, end_date)
            best_products = self.model.get_best_products(start_date, end_date)
            worst_products = self.model.get_worst_products(start_date, end_date)

            # Actualizar la vista
            self.view.populate_clientes(clientes)
            self.view.populate_productos(productos)
            self.view.actualizar_tabla(detalle_ventas)
            self.view.update_summary(total_ventas, total_pedidos, top_producto, top_cliente)
            self.view.update_graphs([], top_clientes, best_products, worst_products)

        except Exception as e:
            self.view.show_error(f"Error: {e}")

    def exportar_a_excel(self):
        """Export table data to Excel file with file dialog"""
        try:
            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            
            file_path = self.view.get_export_path()
            if not file_path:
                return

            self.model.export_to_excel(start_date, end_date, file_path)
            self.view.show_info(f"Reporte exportado exitosamente a {file_path}")

        except Exception as e:
            self.view.show_error(f"Error al exportar a Excel: {e}")

    def __del__(self):
        """Cerrar la conexión al destruir el controlador"""
        self.model.close()
