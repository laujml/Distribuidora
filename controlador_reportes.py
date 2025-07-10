from modelo_reportes import ReportesModel

class ReportesController:
    def __init__(self, view):
        self.model = ReportesModel()
        self.view = view
        self.view.btn_exportar.clicked.connect(self.exportar_a_excel)
        self.view.btn_actualizar.clicked.connect(self.actualizar_datos)
        self.mostrar_reporte("Semanal")  # Valor por defecto

    def mostrar_reporte(self, periodo):
        self.view.set_periodo(periodo)
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = self.model.adjust_date_range(end_date, periodo)

        # Datos de ventas por fecha
        ventas = self.model.get_ventas_por_fecha(start_date, end_date)
        fechas = [v[0] for v in ventas]
        totales = [v[1] for v in ventas]
        self.view.actualizar_grafico_ventas(fechas, totales)

        # Top clientes
        top_clientes = self.model.get_top_clientes(start_date, end_date)
        clientes = [c[0] for c in top_clientes]
        totales_clientes = [c[1] for c in top_clientes]
        self.view.actualizar_grafico_top_clientes(clientes, totales_clientes)

        # Productos más y menos vendidos
        productos_vendidos = self.model.get_productos_vendidos(start_date, end_date)
        productos = [p[0] for p in productos_vendidos]
        cantidades = [p[1] for p in productos_vendidos]
        self.view.actualizar_grafico_productos(productos, cantidades)

        # Detalle de ventas para la tabla
        detalle_ventas = self.model.get_detalle_ventas(start_date, end_date)
        self.view.actualizar_tabla(detalle_ventas)

    def exportar_a_excel(self):
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = self.model.adjust_date_range(end_date, self.view.periodo)
        self.model.export_to_excel(start_date, end_date)

    def actualizar_datos(self):
        self.model.close()
        self.model = ReportesModel()
        self.mostrar_reporte(self.view.periodo)
