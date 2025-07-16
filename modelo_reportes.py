import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from modelo.db_config import conectar

class ReportesModel:
    def __init__(self):
        """
        Inicializa la conexión con la base de datos.
        """
        try:
            self.conn = conectar()
        except Exception as e:
            raise e

    def get_clientes(self):
        """
        Obtiene la lista de clientes de la base de datos.

        Returns:
            Una lista de tuplas con el ID y nombre de cada cliente.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente")
            clientes = [(str(id_cliente), nombre) for id_cliente, nombre in cursor.fetchall()]
            cursor.close()
            return clientes
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener clientes: {e}")

    def get_productos(self):
        """
        Obtiene la lista de productos de la base de datos.

        Returns:
            Una lista de tuplas con el ID y descripción de cada producto.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Productos, descripcion FROM Productos")
            productos = [(id_producto, desc) for id_producto, desc in cursor.fetchall()]
            cursor.close()
            return productos
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener productos: {e}")

    def get_total_ventas(self, start_date, end_date, cliente_id=None):
        """
        Obtiene el total de ventas y el número de pedidos en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.
            cliente_id (str, optional): ID del cliente. Defaults to None.

        Returns:
            Una tupla con el total de ventas y el número de pedidos.
        """
        try:
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
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener total de ventas: {e}")

    def get_top_cliente(self, start_date, end_date):
        """
        Obtiene el cliente con el mayor total de ventas en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.

        Returns:
            El nombre del cliente con el mayor total de ventas.
        """
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
        """
        Obtiene la lista de productos vendidos en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.
            producto_id (str, optional): ID del producto. Defaults to None.

        Returns:
            Una lista de tuplas con la descripción del producto y la cantidad vendida.
        """
        try:
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
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener productos vendidos: {e}")

    def get_detalle_ventas(self, start_date, end_date, limit=1000):
        """
        Obtiene el detalle de las ventas en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.
            limit (int, optional): Límite de filas a obtener. Defaults to 1000.

        Returns:
            Una lista de tuplas con la fecha, cliente, producto, cantidad y subtotal de cada venta.
        """
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
        """
        Obtiene las ventas totales por fecha en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.

        Returns:
            Una lista de tuplas con la fecha y el total de ventas.
        """
        try:
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
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener ventas por fecha: {e}")

    def get_top_clientes(self, start_date, end_date, limit=5):
        """
        Obtiene los clientes con el mayor total de ventas en un rango de fechas.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.
            limit (int, optional): Número de clientes a obtener. Defaults to 5.

        Returns:
            Una lista de tuplas con el nombre del cliente y el total de ventas.
        """
        try:
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
        except mysql.connector.Error as e:
            raise Exception(f"Error al obtener top clientes: {e}")

    def export_to_excel(self, start_date, end_date, filepath="reporte_ventas.xlsx"):
        """
        Exporta el detalle de las ventas a un archivo Excel.

        Args:
            start_date (str): Fecha de inicio del rango.
            end_date (str): Fecha de fin del rango.
            filepath (str, optional): Ruta del archivo Excel. Defaults to "reporte_ventas.xlsx".

        Returns:
            True si la exportación fue exitosa, False en caso contrario.
        """
        try:
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
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn.is_connected():
            self.conn.close()

    def adjust_date_range(self, end_date, period):
        """
        Ajusta la fecha de inicio según el período seleccionado.

        Args:
            end_date (str): Fecha de fin del rango.
            period (str): Período seleccionado ("Semanal" o "Mensual").

        Returns:
            La fecha de inicio del rango.
        """
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if period == "Semanal":
                start_dt = end_dt - timedelta(days=6)
            else:  # Mensual
                start_dt = end_dt - timedelta(days=30)
            return start_dt.strftime("%Y-%m-%d")
        except ValueError as e:
            raise Exception(f"Formato de fecha inválido: {e}")
