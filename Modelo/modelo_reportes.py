import pymysql
from datetime import datetime, timedelta
import pandas as pd
import os
from decimal import Decimal
from Modelo.db_config import conectar

class ReportesModel:
    def __init__(self):
        try:
            self.conn = conectar()
        except Exception as e:
            raise Exception(f"Error al conectar a la base de datos: {e}")

    def get_clientes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente ORDER BY Nombre")
            # Convertir a string el ID para evitar problemas
            clientes = [(str(id_cliente), nombre) for id_cliente, nombre in cursor.fetchall()]
            cursor.close()
            return clientes
        except pymysql.Error as e:
            raise Exception(f"Error al obtener clientes: {e}")

    def get_productos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ID_Productos, descripcion FROM Productos ORDER BY descripcion")
            productos = [(str(id_producto), desc) for id_producto, desc in cursor.fetchall()]
            cursor.close()
            return productos
        except pymysql.Error as e:
            raise Exception(f"Error al obtener productos: {e}")

    def get_total_ventas(self, start_date, end_date, cliente_id=None):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT 
                    COALESCE(SUM(dp.subtotal), 0) as total_ventas, 
                    COUNT(DISTINCT p.ID_Pedido) as total_pedidos
                FROM detalle_pedido dp
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            
            if cliente_id and cliente_id != "":
                query += " AND p.ID_Cliente = %s"
                params.append(int(cliente_id))
                
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()

                    # Verificar qué devuelve la consulta
            print(f"Consulta de total_ventas y total_pedidos: {query} con params {params}")
            print(f"Resultado de la consulta: {result}")
            
            # Convertir Decimal a float correctamente
            total_ventas = float(result[0]) if result[0] is not None else 0.0
            total_pedidos = int(result[1]) if result[1] is not None else 0
            
            return total_ventas, total_pedidos
        except (pymysql.Error, ValueError) as e:
            raise Exception(f"Error al obtener total de ventas: {e}")

    def get_top_cliente(self, start_date, end_date):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT c.Nombre, SUM(dp.subtotal) as total
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                ORDER BY total DESC
                LIMIT 1
            """
            cursor.execute(query, [start_date, end_date])
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 'Sin datos'
        except pymysql.Error as e:
            raise Exception(f"Error al obtener cliente top: {e}")

    def get_top_product(self, start_date, end_date):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT pr.descripcion, SUM(dp.cantidad_pares) as cantidad
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                ORDER BY cantidad DESC
                LIMIT 1
            """
            cursor.execute(query, [start_date, end_date])
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 'Sin datos'
        except pymysql.Error as e:
            raise Exception(f"Error al obtener producto top: {e}")

    def get_top_clientes(self, start_date, end_date, limit=5):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT c.Nombre, SUM(dp.subtotal) as total
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                GROUP BY c.ID_Cliente, c.Nombre
                HAVING total > 0
                ORDER BY total DESC
                LIMIT %s
            """
            cursor.execute(query, [start_date, end_date, limit])
            # Convertir Decimal a float y truncar nombres largos
            result = []
            for row in cursor.fetchall():
                nombre = row[0][:15] + '...' if len(row[0]) > 15 else row[0]
                total = float(row[1]) if isinstance(row[1], Decimal) else row[1]
                result.append((nombre, total))
            cursor.close()
            return result
        except pymysql.Error as e:
            raise Exception(f"Error al obtener top clientes: {e}")

    def get_best_products(self, start_date, end_date, limit=5):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT pr.descripcion, SUM(dp.cantidad_pares) as cantidad
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                HAVING cantidad > 0
                ORDER BY cantidad DESC
                LIMIT %s
            """
            cursor.execute(query, [start_date, end_date, limit])
            # Truncar nombres largos de productos
            result = []
            for row in cursor.fetchall():
                descripcion = row[0][:12] + '...' if len(row[0]) > 12 else row[0]
                cantidad = int(row[1]) if row[1] is not None else 0
                result.append((descripcion, cantidad))
            cursor.close()
            return result
        except pymysql.Error as e:
            raise Exception(f"Error al obtener productos más vendidos: {e}")

    def get_worst_products(self, start_date, end_date, limit=5):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT pr.descripcion, SUM(dp.cantidad_pares) as cantidad
                FROM detalle_pedido dp
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                GROUP BY pr.ID_Productos, pr.descripcion
                HAVING cantidad > 0
                ORDER BY cantidad ASC
                LIMIT %s
            """
            cursor.execute(query, [start_date, end_date, limit])
            # Truncar nombres largos de productos
            result = []
            for row in cursor.fetchall():
                descripcion = row[0][:12] + '...' if len(row[0]) > 12 else row[0]
                cantidad = int(row[1]) if row[1] is not None else 0
                result.append((descripcion, cantidad))
            cursor.close()
            return result
        except pymysql.Error as e:
            raise Exception(f"Error al obtener productos menos vendidos: {e}")

    def get_detalle_ventas(self, start_date, end_date, cliente_id=None, producto_id=None, limit=1000):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT 
                    DATE_FORMAT(p.fecha_hora, '%Y-%m-%d %H:%i') as fecha,
                    c.Nombre, 
                    pr.descripcion, 
                    dp.cantidad_pares, 
                    dp.subtotal
                FROM Pedido p
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            
            if cliente_id and cliente_id != "":
                query += " AND p.ID_Cliente = %s"
                params.append(int(cliente_id))
            if producto_id and producto_id != "":
                query += " AND dp.ID_Productos = %s"
                params.append(int(producto_id))
                
            query += " ORDER BY p.fecha_hora DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            # Convertir Decimal a float
            result = []
            for row in cursor.fetchall():
                fecha, cliente, producto, cantidad, subtotal = row
                subtotal_float = float(subtotal) if isinstance(subtotal, Decimal) else subtotal
                result.append((fecha, cliente, producto, cantidad, subtotal_float))
            cursor.close()
            return result
        except (pymysql.Error, ValueError) as e:
            raise Exception(f"Error al obtener detalle de ventas: {e}")

    def export_to_excel(self, start_date, end_date, filepath=None):
        try:
            if filepath is None:
                filepath = os.path.join(os.path.expanduser("~"), "reporte_ventas.xlsx")
                
            cursor = self.conn.cursor()
            query = """
                SELECT 
                    DATE_FORMAT(p.fecha_hora, '%Y-%m-%d %H:%i') as Fecha,
                    c.Nombre as Cliente, 
                    pr.descripcion as Producto, 
                    dp.cantidad_pares as Cantidad, 
                    dp.subtotal as Subtotal
                FROM detalle_pedido dp
                JOIN Pedido p ON dp.ID_Pedido = p.ID_Pedido
                JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
                JOIN Productos pr ON dp.ID_Productos = pr.ID_Productos
                WHERE DATE(p.fecha_hora) BETWEEN %s AND %s
                ORDER BY p.fecha_hora DESC
            """
            cursor.execute(query, [start_date, end_date])
            
            # Convertir los datos
            data = []
            for row in cursor.fetchall():
                fecha, cliente, producto, cantidad, subtotal = row
                subtotal_float = float(subtotal) if isinstance(subtotal, Decimal) else subtotal
                data.append((fecha, cliente, producto, cantidad, subtotal_float))
            
            cursor.close()
            
            if not data:
                raise Exception("No hay datos para exportar en el rango de fechas seleccionado")
            
            # Crear DataFrame y exportar
            df = pd.DataFrame(data, columns=["Fecha", "Cliente", "Producto", "Cantidad", "Subtotal"])
            df.to_excel(filepath, index=False, engine='openpyxl')
            return True
            
        except Exception as e:
            raise Exception(f"Error al exportar a Excel: {e}")

    def adjust_date_range(self, end_date, period):
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if period == "Semanal":
                start_dt = end_dt - timedelta(days=6)  # 7 días incluyendo el día actual
            else:  # Mensual
                start_dt = end_dt - timedelta(days=29)  # 30 días incluyendo el día actual
            return start_dt.strftime("%Y-%m-%d")
        except ValueError as e:
            raise Exception(f"Formato de fecha inválido: {e}")

    def close(self):
        """Cerrar la conexión de base de datos"""
        try:
            if self.conn and hasattr(self.conn, 'close'):
                self.conn.close()
        except Exception:
            pass  # Ignorar errores al cerrar
