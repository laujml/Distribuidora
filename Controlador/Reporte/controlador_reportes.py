import pymysql
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Styles import Styles
import pandas as pd
import os
from vista_reportes import ReportesView

class ReportesController:
    def __init__(self, view, conectar_func):
        self.view = view
        self.stack = None
        self.conectar = conectar_func
        self.setup_connections()
    
    def set_stack(self, stack):
        """Asignar el stack widget para poder navegar"""
        self.stack = stack
    
    def setup_connections(self):
        """Configurar las conexiones de los botones"""
        self.view.period_cb.currentTextChanged.connect(self.on_period_changed)
        if hasattr(self.view, 'btn_regresar'):
            self.view.btn_regresar.clicked.connect(self.regresar_a_seleccion)
        if hasattr(self.view, 'btn_actualizar'):
            self.view.btn_actualizar.clicked.connect(self.actualizar_datos)
        if hasattr(self.view, 'btn_exportar'):
            self.view.btn_exportar.clicked.connect(self.exportar_a_excel)
    
    def mostrar_reporte(self, periodo):
        """Mostrar reporte del período especificado"""
        self.view.set_periodo(periodo)
        self.actualizar_datos()
    
    def on_period_changed(self, nuevo_periodo):
        """Manejar cambio de período en el ComboBox"""
        self.view.titulo.setText(f"Reporte {nuevo_periodo}")
        self.actualizar_datos()
    
    def regresar_a_seleccion(self):
        """Regresar a la pantalla de selección inicial"""
        if self.stack:
            self.stack.setCurrentIndex(0)
    
    def actualizar_datos(self):
        """Fetch data from database and update view"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            filters = self.view.get_filter_values()
            start_date = filters['start_date']
            end_date = filters['end_date']
            cliente_id = filters['cliente_id']
            producto_id = filters['producto_id']
            period = filters['period']

            cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente")
            clientes = cursor.fetchall()
            self.view.populate_clientes(clientes)

            cursor.execute("SELECT ID_Productos, descripcion FROM Productos")
            productos = cursor.fetchall()
            self.view.populate_productos(productos)

            query = """
                SELECT p.fecha_hora, c.Nombre, pr.descripcion, dp.cantidad_pares, dp.subtotal
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE p.fecha_hora BETWEEN %s AND %s
            """
            params = [start_date, end_date]

            if cliente_id:
                query += " AND p.ID_Cliente = %s"
                params.append(cliente_id)
            if producto_id:
                query += " AND dp.ID_Productos = %s"
                params.append(producto_id)

            cursor.execute(query, params)
            datos = cursor.fetchall()
            self.view.actualizar_tabla(datos)

            total_ventas = sum(row[4] for row in datos) if datos else 0.0
            total_pedidos = len(set(row[0] for row in datos)) if datos else 0

            cursor.execute("""
                SELECT c.Nombre, SUM(dp.subtotal) as total
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                ORDER BY total DESC
                LIMIT 1
            """, [start_date, end_date])
            top_cliente = cursor.fetchone()
            top_cliente_name = top_cliente[0] if top_cliente else "-"

            cursor.execute("""
                SELECT pr.descripcion, SUM(dp.cantidad_pares) as cantidad
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                ORDER BY cantidad DESC
                LIMIT 1
            """, [start_date, end_date])
            top_producto = cursor.fetchone()
            top_producto_name = top_producto[0] if top_producto else "-"

            self.view.update_summary(total_ventas, total_pedidos, top_producto_name, top_cliente_name)

            cursor.execute("""
                SELECT c.Nombre, SUM(dp.subtotal)
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                ORDER BY SUM(dp.subtotal) DESC
                LIMIT 5
            """, [start_date, end_date])
            client_data = [(row[0], row[1]) for row in cursor.fetchall()]

            cursor.execute("""
                SELECT pr.descripcion, SUM(dp.cantidad_pares)
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                ORDER BY SUM(dp.cantidad_pares) DESC
                LIMIT 5
            """, [start_date, end_date])
            best_products = [(row[0], row[1]) for row in cursor.fetchall()]

            cursor.execute("""
                SELECT pr.descripcion, SUM(dp.cantidad_pares)
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                ORDER BY SUM(dp.cantidad_pares) ASC
                LIMIT 5
            """, [start_date, end_date])
            worst_products = [(row[0], row[1]) for row in cursor.fetchall()]

            self.view.update_graphs([], client_data, best_products, worst_products)

            cursor.close()
            conn.close()

        except pymysql.Error as err:
            self.view.show_error(f"Error de base de datos: {err}")
        except Exception as e:
            self.view.show_error(f"Error: {e}")

    def exportar_a_excel(self):
        try:
            data = self.view.get_table_data_for_export()
            if not data or not data[1:]:  
                self.view.show_error("No hay datos para exportar.")
                return

            # Crear DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

           
            default_path = os.path.join(os.getcwd(), "reporte_ventas.xlsx")
            file_path, _ = QFileDialog.getSaveFileName(
                self.view, "Guardar Reporte", default_path, "Excel Files (*.xlsx)"
            )
            if not file_path:  
                return

            # Export to Excel
            df.to_excel(file_path, index=False)
            self.view.show_info(f"Reporte exportado exitosamente a {file_path}")

        except PermissionError:
            self.view.show_error("No se puede guardar el archivo. Cierre el archivo Excel si está abierto.")
        except Exception as e:
            self.view.show_error(f"Error al exportar a Excel: {e}")
