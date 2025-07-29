from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QDate
from Modelo.modelo_reportes import ReportesModel
from Vista.Reporte.vista_reportes import ReportesView

class ReportesController:
    def __init__(self, view: ReportesView, conectar_func):
        self.view = view
        self.model = None
        self.stack = None
        self.conectar_func = conectar_func
        self.setup_connections()
        self.initialize_model()

    def initialize_model(self):
        """Inicializar el modelo con manejo de errores"""
        try:
            self.model = ReportesModel()
        except Exception as e:
            self.view.show_error(f"Error al conectar con la base de datos: {e}")
            return False
        return True

    def set_stack(self, stack):
        """Asignar el stack widget para poder navegar"""
        self.stack = stack

    def setup_connections(self):
        """Configurar las conexiones de los botones"""
        self.view.period_changed.connect(self.on_period_changed)
        
        # Conectar botones si existen
        if hasattr(self.view, 'btn_regresar'):
            self.view.btn_regresar.clicked.connect(self.regresar_a_seleccion)
        if hasattr(self.view, 'btn_actualizar'):
            print("Conectando botón de actualizar")
            self.view.btn_actualizar.clicked.connect(self.actualizar_datos)  # Conectar
        if hasattr(self.view, 'btn_exportar'):
            self.view.btn_exportar.clicked.connect(self.exportar_a_excel)
        if hasattr(self.view, 'btn_calendario'):
            self.view.btn_calendario.clicked.connect(self.mostrar_selector_fechas)

        #Conectar señal de recarga si existe en la vista
        if hasattr(self.view, 'recargar_reportes'):
            self.view.recargar_reportes.connect(self.recargar_reportes_completo)    

    def recargar_reportes_completo(self):
        """Recargar completamente la vista y reconectar con la base de datos"""
        try:
            print("Iniciando recarga completa de reportes...")
            
            # 1. Limpiar la vista actual
            if hasattr(self.view, 'limpiar_vista'):
                self.view.limpiar_vista()
            
            # 2. Cerrar modelo anterior si existe
            if self.model:
                try:
                    self.model.close()
                    print("Modelo anterior cerrado correctamente")
                except Exception as e:
                    print(f"Error al cerrar modelo anterior: {e}")
            
            # 3. Reinicializar el modelo con nueva conexión
            self.model = None
            if not self.initialize_model():
                self.view.show_error("No se pudo reinicializar la conexión a la base de datos")
                return
                
            print("Nuevo modelo inicializado correctamente")
            
            # 4. Recargar todos los datos
            self.actualizar_datos()
            
            # 5. Mostrar mensaje de confirmación
            self.view.show_info("Reportes actualizados correctamente")
            print("Recarga completa finalizada exitosamente")
            
        except Exception as e:
            error_msg = f"Error al recargar reportes: {str(e)}"
            print(error_msg)
            self.view.show_error(error_msg)

    def disconnect_all_signals(self):
        """Desconectar todas las señales (método de utilidad)"""
        try:
            # Desconectar señales principales
            if hasattr(self.view, 'period_changed'):
                self.view.period_changed.disconnect()
            if hasattr(self.view, 'btn_actualizar'):
                self.view.btn_actualizar.clicked.disconnect()
            if hasattr(self.view, 'btn_exportar'):
                self.view.btn_exportar.clicked.disconnect()
            if hasattr(self.view, 'btn_calendario'):
                self.view.btn_calendario.clicked.disconnect()
            if hasattr(self.view, 'btn_regresar'):
                self.view.btn_regresar.clicked.disconnect()
            if hasattr(self.view, 'recargar_reportes'):
                self.view.recargar_reportes.disconnect()
        except Exception as e:
            print(f"Error al desconectar señales: {e}")

    def reconectar_signals(self):
        """Reconectar todas las señales después de una recarga"""
        try:
            self.setup_connections()
            print("Señales reconectadas correctamente")
        except Exception as e:
            print(f"Error al reconectar señales: {e}")

    def mostrar_selector_fechas(self):
        """Mostrar un diálogo para seleccionar fechas personalizadas"""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit
            from PyQt6.QtCore import QDate
            
            dialog = QDialog(self.view)
            dialog.setWindowTitle("Seleccionar Rango de Fechas")
            dialog.setModal(True)
            dialog.resize(300, 150)
            
        # AGREGAR ESTILO PARA CAMBIAR EL COLOR DEL TEXTO
            dialog.setStyleSheet("""
                QDateEdit {
                    color: #000000;  /* Texto negro */
                    background-color: #ffffff;  /* Fondo blanco */
                    border: 1px solid #cccccc;
                    padding: 5px;
                    font-size: 12px;
                }
                QDateEdit:focus {
                    border: 2px solid #4d5a62;
                }
                QLabel {
                    color: #000000;  /* Texto negro */
                    font-weight: bold;
                }
                QPushButton {
                    color: #ffffff;  /* Letras blancas */
                    background-color: #4d5a62;  /* Fondo gris oscuro */
                    border: 1px solid #4d5a62;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #6c757d;  /* Fondo gris más claro al pasar el mouse */
                }
                QPushButton:pressed {
                    background-color: #343a40;  /* Fondo más oscuro al presionar */
                }
                """)

            layout = QVBoxLayout()
            
            # Fecha inicio
            layout.addWidget(QLabel("Fecha de inicio:"))
            fecha_inicio = QDateEdit()
            fecha_inicio.setCalendarPopup(True)
            fecha_inicio.setDate(self.view.fecha_inicio.date())
            layout.addWidget(fecha_inicio)
            
            # Fecha fin
            layout.addWidget(QLabel("Fecha de fin:"))
            fecha_fin = QDateEdit()
            fecha_fin.setCalendarPopup(True)
            fecha_fin.setDate(self.view.fecha_fin.date())
            layout.addWidget(fecha_fin)
            
            # Botones
            buttons_layout = QHBoxLayout()
            btn_aceptar = QPushButton("Aceptar")
            btn_cancelar = QPushButton("Cancelar")
            
            def aceptar():
                self.view.fecha_inicio.setDate(fecha_inicio.date())
                self.view.fecha_fin.setDate(fecha_fin.date())
                self.view.actualizar_label_fechas()
                self.actualizar_datos()
                dialog.accept()
            
            btn_aceptar.clicked.connect(aceptar)
            btn_cancelar.clicked.connect(dialog.reject)
            
            buttons_layout.addWidget(btn_aceptar)
            buttons_layout.addWidget(btn_cancelar)
            layout.addLayout(buttons_layout)
            
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            self.view.show_error(f"Error al mostrar selector de fechas: {e}")
    
    def mostrar_reporte(self, periodo):
        """Mostrar reporte del período especificado"""
        if not self.model:
            if not self.initialize_model():
                return
                
        try:
            self.set_periodo(periodo)
            self.recargar_reportes_completo()
        except Exception as e:
            self.view.show_error(f"Error al mostrar reporte: {e}")

    def set_periodo(self, periodo):
        """Establecer período y fechas"""
        try:
            self.view.set_periodo(periodo)
            fecha_actual = QDate.currentDate()
            end_date = fecha_actual.toString("yyyy-MM-dd")
            start_date = self.model.adjust_date_range(end_date, periodo)
            
            # Actualizar las fechas en la vista
            self.view.set_start_date(start_date)
            self.view.fecha_fin.setDate(fecha_actual)
            self.view.actualizar_label_fechas()
            
        except Exception as e:
            self.view.show_error(f"Error al establecer período: {e}")

    def on_period_changed(self, nuevo_periodo):
        """Manejar cambio de período"""
        try:
            self.set_periodo(nuevo_periodo)
            self.recargar_reportes_completo()
        except Exception as e:
            self.view.show_error(f"Error al cambiar período: {e}")

    def regresar_a_seleccion(self):
        """Regresar a la pantalla de selección inicial"""
        if self.stack:
            self.stack.setCurrentIndex(0)

    def actualizar_datos(self):
        """Obtener datos del modelo y actualizar vista"""
        if not self.model:
            if not self.initialize_model():
                return
                    
        try:
            # Obtener filtros actuales
            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            cliente_id = filters.get('cliente_id', '')
            producto_id = filters.get('producto_id', '')

            # Validar fechas
            if not start_date or not end_date:
                self.view.show_error("Las fechas no son válidas")
                return

            # Obtener datos del modelo
            print(f"Obteniendo datos para: {start_date} a {end_date}")  # Debug
            
            # Obtener listas para combos
            clientes = self.model.get_clientes()
            productos = self.model.get_productos()
            
            # Obtener métricas principales (totales de ventas y pedidos)
            total_ventas, total_pedidos = self.model.get_total_ventas(start_date, end_date, cliente_id)
            top_cliente = self.model.get_top_cliente(start_date, end_date)
            top_producto = self.model.get_top_product(start_date, end_date)
            
            # Obtener datos para gráficos
            top_clientes = self.model.get_top_clientes(start_date, end_date)
            best_products = self.model.get_best_products(start_date, end_date)
            worst_products = self.model.get_worst_products(start_date, end_date)
            
            # Obtener detalle de ventas
            detalle_ventas = self.model.get_detalle_ventas(start_date, end_date, cliente_id, producto_id)

            print(f"Datos obtenidos: Ventas={total_ventas}, Pedidos={total_pedidos}")  # Debug
            print(f"Top clientes: {len(top_clientes)}, Mejores productos: {len(best_products)}")  # Debug

            # Actualizar la vista
            self.view.populate_clientes(clientes)
            self.view.populate_productos(productos)
            self.view.update_summary(total_ventas, total_pedidos, top_producto, top_cliente)  # Actualiza los totales
            self.view.actualizar_tabla(detalle_ventas)
            
            # Actualizar gráficos - pasar lista vacía como primer parámetro por compatibilidad
            self.view.update_graphs([], top_clientes, best_products, worst_products)

            print("Vista actualizada correctamente")  # Debug

        except Exception as e:
            error_msg = f"Error al actualizar datos: {str(e)}"
            print(error_msg)  # Debug
            self.view.show_error(error_msg)


    def exportar_a_excel(self):
        """Exportar datos a Excel con diálogo de archivo"""
        if not self.model:
            if not self.initialize_model():
                return
                
        try:
            # Obtener filtros actuales
            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            
            # Obtener ruta de archivo
            file_path = self.view.get_export_path()
            if not file_path:
                return  # Usuario canceló

            # Validar extensión
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'

            # Exportar datos
            self.model.export_to_excel(start_date, end_date, file_path)
            self.view.show_info(f"Reporte exportado exitosamente a:\n{file_path}")

        except Exception as e:
            self.view.show_error(f"Error al exportar a Excel: {e}")

    def __del__(self):
        """Cerrar la conexión al destruir el controlador"""
        try:
            if self.model:
                self.model.close()
        except Exception:
            pass  # Ignorar errores al cerrar
