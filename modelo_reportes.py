import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from modelo.db_config import DatabaseConnection

class ReportesModel:
    def __init__(self):
        try:
            self.db = DatabaseConnection()
            self.conn = self.db.get_connection()
        except mysql.connector.Error as e:
            raise Exception(f"Error connecting to MariaDB: {e}")

    def get_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente")
        clientes = [(id_cliente, nombre) for id_cliente, nombre in cursor.fetchall()]
        cursor.close()
        return clientes

    def get_productos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ID_Productos, descripcion FROM Productos")
        productos = [(id_producto, desc) for id_producto, desc in cursor.fetchall()]
        cursor.close()
        return productos

    def get_total_ventas(self, start_date, end_date, cliente_id=None):
        cursor = self.conn.cursor()
        query = """
            SELECT SUM(p.total) as total_ventas, COUNT(p.ID_Pedido) as total_pedidos
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
        return result[0] or 0, result[1] or 0

    def get_top_cliente(self, start_date, end_date):
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

    def get_productos_vendidos(self, start_date, end_date, producto_id=None):
        cursor = self.conn.cursor()
        query = """
            SELECT pr.descripcion, SUM(dp.cantidad_pares) as total_pares
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

    def get_detalle_ventas(self, start_date, end_date):
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
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_ventas_por_fecha(self, start_date, end_date):
        cursor = self.conn.cursor()
        query = """
            SELECT DATE(p.fecha_hora) as fecha, SUM(p.total) as total
            FROM Pedido p
            WHERE p.fecha_hora BETWEEN %s AND %s
            GROUP BY DATE(p.fecha_hora)
        """
        cursor.execute(query, [start_date, end_date])
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_top_clientes(self, start_date, end_date, limit=5):
        cursor = self.conn.cursor()
        query = """
            SELECT c.Nombre, SUM(p.total) as total
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

    def export_to_excel(self, start_date, end_date):
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
        df = pd.DataFrame(data, columns=["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
        df.to_excel(r"C:\Users\jflor\OneDrive\Documents\ReportesProyectoApps\reporte_ventas.xlsx", index=False)

    def close(self):
        self.db.close()

    def adjust_date_range(self, end_date, period):
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if period == "Semanal":
            start_dt = end_dt - timedelta(days=6)
        else:  # Mensual
            start_dt = end_dt - timedelta(days=30)
        return start_dt.strftime("%Y-%m-%d")
