# Modelo/ProductoModel.py
import mysql.connector
from Modelo.db_config import conectar

class ProductoModel:
    """Modelo para la gestión de productos - Solo consultas SQL"""
    
    def __init__(self):
        pass
    
    def conectar_db(self):
        """Establece conexión con la base de datos"""
        return conectar()
    
    def insertar_producto(self, datos_producto):
        """Inserta un nuevo producto en la base de datos"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        sql = """INSERT INTO productos 
        (ID_Productos, descripcion, precio, talla, color, stockActual, fecha_ingreso, ID_Proveedor) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, datos_producto)
        conn.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        return filas_afectadas
    
    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        sql = "DELETE FROM productos WHERE ID_Productos = %s"
        cursor.execute(sql, (id_producto,))
        conn.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        return filas_afectadas
    
    def actualizar_producto(self, datos_producto):
        """Actualiza un producto existente"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        sql = """UPDATE productos SET descripcion=%s, precio=%s, talla=%s, color=%s, 
                 stockActual=%s, fecha_ingreso=%s, ID_Proveedor=%s 
                 WHERE ID_Productos=%s"""
        
        cursor.execute(sql, datos_producto)
        conn.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        conn.close()
        return filas_afectadas
    
    def buscar_producto_por_id(self, id_producto):
        """Busca un producto por su ID"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM productos WHERE ID_Productos = %s"
        cursor.execute(sql, (id_producto,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado
    
    def obtener_todos_productos(self):
        """Obtiene todos los productos de la base de datos"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return productos
    
    def insertar_productos_masivo(self, lista_productos):
        """Inserta múltiples productos de forma masiva"""
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        sql_insert = """INSERT INTO productos 
        (ID_Productos, descripcion, precio, talla, color, stockActual, fecha_ingreso, ID_Proveedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        sql_update = """UPDATE productos SET descripcion=%s, precio=%s, talla=%s, color=%s,
        stockActual=%s, fecha_ingreso=%s, ID_Proveedor=%s WHERE ID_Productos=%s"""
        
        productos_insertados = 0
        productos_actualizados = 0
        
        for producto in lista_productos:
            # Verificar si existe
            cursor.execute("SELECT * FROM productos WHERE ID_Productos = %s", (producto[0],))
            existe = cursor.fetchone()
            
            if existe:
                cursor.execute(sql_update, producto[1:] + (producto[0],))
                productos_actualizados += 1
            else:
                cursor.execute(sql_insert, producto)
                productos_insertados += 1
        
        conn.commit()
        cursor.close()
        conn.close()
        return productos_insertados, productos_actualizados
