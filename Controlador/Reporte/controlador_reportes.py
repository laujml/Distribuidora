import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import os  
from db_config import conectar

class ReportesModel:
    def __init__(self):
        # Inicia la conexión a la base de datos
        try:
            self.conn = conectar()
        except Exception as e:
            raise e

    def get_clientes(self):
        # Obtiene la lista de clientes desde la base de datos
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente")
            clientes = [(str(id_cliente), nombre) for id_cliente, nombre in cursor.fetchall()]
            cursor.close()
            return clientes
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener clientes: {e}")

    def get_productos(self):
        # Obtiene la lista de productos desde la base de datos
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Productos, descripcion FROM Productos")
            productos = [(id_producto, desc) for id_producto, desc in cursor.fetchall()]
            cursor.close()
            return productos
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener productos: {e}")

    def get_total_ventas(self, start_date, end_date, cliente_id=None):
        # Retorna el total de ventas y el total de pedidos en el rango de fechas
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT IFNULL(SUM(p.total), 0) as total_ventas, COUNT(p.ID_Pedido) as total_pedidos
                FROM Pedido p
                WHERE p.fecha_hora BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            if cliente_id:
                query += " AND p.ID_Cliente = %s"
                params.append(cliente_id)
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            # Verifica que los totales sean correctos y no None
            total_ventas = result[0] if result and result[0] is not None else 0
            total_pedidos = result[1] if result and result[1] is not None else 0
            return total_ventas, total_pedidos
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener total de ventas: {e}")

    def get_top_cliente(self, start_date, end_date):
        # Retorna el cliente con mayor monto de ventas en el rango de fechas
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT c.Nombre, SUM(p.total) as total
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                ORDER BY total DESC
                LIMIT 1
            """
            cursor.execute(query, [start_date, end_date])
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else '-'
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener cliente top: {e}")

    def get_productos_vendidos(self, start_date, end_date, producto_id=None):
        # Retorna la lista de productos vendidos y la suma de pares por producto
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT pr.descripcion, IFNULL(SUM(dp.cantidad_pares), 0) as total_pares
                FROM detalle_pedido dp
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE p.fecha_hora BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            if producto_id:
                query += " AND dp.ID_Productos = %s"
                params.append(producto_id)
            query += " GROUP BY pr.ID_Productos, pr.descripcion ORDER BY total_pares"
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener productos vendidos: {e}")

    def get_detalle_ventas(self, start_date, end_date, limit=1000):
        # Retorna el detalle de ventas en el rango de fechas
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT p.fecha_hora, c.Nombre, pr.descripcion, dp.cantidad_pares, dp.subtotal
                FROM detalle_pedido dp
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE p.fecha_hora BETWEEN %s AND %s
                LIMIT %s
            """
            cursor.execute(query, [start_date, end_date, limit])
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener detalle de ventas: {e}")

    def get_ventas_por_fecha(self, start_date, end_date):
        # Retorna la suma total de ventas agrupadas por fecha
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT DATE(p.fecha_hora) as fecha, IFNULL(SUM(p.total), 0) as total
                FROM Pedido p
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY DATE(p.fecha_hora)
            """
            cursor.execute(query, [start_date, end_date])
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener ventas por fecha: {e}")

    def get_top_clientes(self, start_date, end_date, limit=5):
        # Retorna los clientes con mayor monto de ventas en el rango de fechas
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT c.Nombre, IFNULL(SUM(p.total), 0) as total
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                WHERE p.fecha_hora BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                ORDER BY total DESC
                LIMIT %s
            """
            cursor.execute(query, [start_date, end_date, limit])
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener top clientes: {e}")

    def export_to_excel(self, start_date, end_date, filepath=None):
        # Exporta el reporte de ventas a un archivo Excel
        try:
            if filepath is None:
                filepath = os.path.join(os.path.expanduser("~"), "reporte_ventas.xlsx")
            cursor = self.conn.cursor()
            query = """
                SELECT p.fecha_hora, c.Nombre, pr.descripcion, dp.cantidad_pares, dp.subtotal
                FROM detalle_pedido dp
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE p.fecha_hora BETWEEN %s AND %s
            """
            cursor.execute(query, [start_date, end_date])
            data = cursor.fetchall()
            cursor.close()
            if not data:
                raise Exception("No hay datos para exportar")
            df = pd.DataFrame(data, columns=["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
            df.to_excel(filepath, index=False)
            return True
        except Exception as e:
            raise Exception(f"Error al exportar a Excel: {e}")

    def close(self):
        # Cierra la conexión a la base de datos
        if self.conn.is_connected():
            self.conn.close()

    def adjust_date_range(self, end_date, period):
        # Ajusta el rango de fechas según el periodo seleccionado (semanal o mensual)
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if period == "Semanal":
                start_dt = end_dt - timedelta(days=6)
            else:  # Mensual
                start_dt = end_dt - timedelta(days=30)
            return start_dt.strftime("%Y-%m-%d")
        except ValueError as e:
            raise Exception(f"Formato de fecha inválido: {e}")
