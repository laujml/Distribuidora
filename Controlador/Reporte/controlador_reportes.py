from Modelo.modelo_reportes import ReportesModel
from Vista.Reporte.vista_reportes import ReportesView

class ReportesController:
    def __init__(self):
        self.model = ReportesModel()
        self.view = ReportesView()
        self.connect_signals()
        self.load_initial_data()

    def connect_signals(self):
        self.view.buscar_btn.clicked.connect(self.update_reports)
        self.view.limpiar_btn.clicked.connect(self.clear_filters)
        self.view.exportar_btn.clicked.connect(self.export_to_excel)
        self.view.actualizar_btn.clicked.connect(self.update_reports)

    def load_initial_data(self):
        clientes = self.model.get_clientes()
        productos = self.model.get_productos()
        self.view.populate_clientes(clientes)
        self.view.populate_productos(productos)
        self.update_reports()

    def update_reports(self):
        filters = self.view.get_filter_values()
        start_date = filters['start_date']
        end_date = filters['end_date']
        cliente_id = filters['cliente_id'] if filters['cliente_id'] else None
        producto_id = filters['producto_id'] if filters['producto_id'] else None
        period = filters['period']

        # Adjust date range for weekly reports
        if period == "Semanal":
            start_date = self.model.adjust_date_range(end_date, period)
            self.view.set_start_date(start_date)

        # Get data from model
        total_ventas, total_pedidos = self.model.get_total_ventas(start_date, end_date, cliente_id)
        top_cliente = self.model.get_top_cliente(start_date, end_date)
        productos_vendidos = self.model.get_productos_vendidos(start_date, end_date, producto_id)
        detalle_ventas = self.model.get_detalle_ventas(start_date, end_date)
        ventas_por_fecha = self.model.get_ventas_por_fecha(start_date, end_date)
        top_clientes = self.model.get_top_clientes(start_date, end_date)

        # Prepare data for graphs
        best_products = productos_vendidos[-5:] if productos_vendidos else []
        worst_products = productos_vendidos[:5] if productos_vendidos else []
        top_producto = productos_vendidos[-1][0] if productos_vendidos else '-'

        # Update view
        self.view.update_summary(total_ventas, total_pedidos, top_producto, top_cliente)
        self.view.update_table(detalle_ventas)
        self.view.update_graphs(ventas_por_fecha, top_clientes, best_products, worst_products)

    def clear_filters(self):
        self.view.reset_filters()
        self.update_reports()

    def export_to_excel(self):
        filters = self.view.get_filter_values()
        self.model.export_to_excel(filters['start_date'], filters['end_date'])

    def show(self):
        self.view.show()

    def close(self):
        self.model.close()
