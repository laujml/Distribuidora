from Modelo.modelo_reportes import ReportesModel

class ReportesController:
    def __init__(self, view=None):
        self.model = None
        self.view = view  # Recibir la vista desde el main
        if self.view:
            self.connect_signals()
            self.load_initial_data()
    
    def connect_signals(self):
        self.view.buscar_btn.clicked.connect(self.update_reports)
        self.view.limpiar_btn.clicked.connect(self.clear_filters)
        self.view.btn_exportar.clicked.connect(self.export_to_excel)
        self.view.btn_actualizar.clicked.connect(self.update_reports)
    
    def load_initial_data(self):
        try:
            self.model = ReportesModel()
            clientes = self.model.get_clientes()
            productos = self.model.get_productos()
            self.view.populate_clientes(clientes)
            self.view.populate_productos(productos)
            self.update_reports()
        except Exception as e:
            self.view.show_error(str(e))
    
    def update_reports(self):
        try:
            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            
            if start_date > end_date:
                self.view.show_error("La fecha de inicio no puede ser posterior a la fecha de fin.")
                return
            
            cliente_id = filters['cliente_id']
            producto_id = filters['producto_id']
            period = filters['period']
            
            if period == "Semanal":
                start_date = self.model.adjust_date_range(end_date, period)
                self.view.set_start_date(start_date)
            
            total_ventas, total_pedidos = self.model.get_total_ventas(start_date, end_date, cliente_id)
            top_cliente = self.model.get_top_cliente(start_date, end_date)
            productos_vendidos = self.model.get_productos_vendidos(start_date, end_date, producto_id)
            detalle_ventas = self.model.get_detalle_ventas(start_date, end_date)
            ventas_por_fecha = self.model.get_ventas_por_fecha(start_date, end_date)
            top_clientes = self.model.get_top_clientes(start_date, end_date)
            
            best_products = productos_vendidos[-5:] if productos_vendidos else []
            worst_products = productos_vendidos[:5] if productos_vendidos else []
            top_producto = best_products[-1][0] if best_products else '-'
            
            self.view.update_summary(total_ventas, total_pedidos, top_producto, top_cliente)
            self.view.actualizar_tabla(detalle_ventas)
            self.view.update_graphs(ventas_por_fecha, top_clientes, best_products, worst_products)
            
        except Exception as e:
            self.view.show_error(str(e))
    
    def clear_filters(self):
        self.view.reset_filters()
        self.update_reports()
    
    def export_to_excel(self):
        try:
            filters = self.view.get_filter_values()
            filepath = self.view.get_export_path()
            if not filepath:
                return
            
            success = self.model.export_to_excel(filters['start_date'], filters['end_date'], filepath)
            if success:
                self.view.show_info("Reporte exportado exitosamente.")
        except Exception as e:
            self.view.show_error(str(e))
    
    def mostrar_reporte(self, period):
        self.view.set_periodo(period)
        self.update_reports()
    
    def close(self):
        if self.model:
            self.model.close()
