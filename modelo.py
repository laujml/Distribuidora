import mysql.connector
from datetime import datetime

class Modelo:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",     
            password="", 
            database="Distribuidora"
        )
        self.cursor = self.conexion.cursor()

    def obtener_productos(self):
        self.cursor.execute("SELECT ID_Productos, descripcion, precio FROM Productos WHERE stockActual > 0")
        return self.cursor.fetchall() #fetchall es para recoger los datos que la consulta hizo
    
    def obtener_clientes(self):
        self.cursor.execute("SELECT ID_Cliente, Nombre FROM Cliente")
        resultados = self.cursor.fetchall()
        return [f"{id} - {nombre}" for id, nombre in resultados] #fetchall es para recoger los datos que la consulta hizo

    def crear_pedido(self, id_cliente, total, estado, pendiente_pagar, plazo_dias):
        fecha_actual = datetime.now()
        self.cursor.execute("""
            INSERT INTO Pedido (ID_Cliente, fecha_hora, total, estado, pendiente_pagar, plazo_dias)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_cliente, fecha_actual, total, estado, pendiente_pagar, plazo_dias))
        self.conexion.commit() #.commit() se usa para guardar permanentemente los cambios realizados en una base de datos
        return self.cursor.lastrowid 
        #lastrowid se usa para obtener el ID (clave primaria) del último registro insertado en la base de datos, justo después de hacer un INSERT

    def agregar_detalle(self, id_pedido, num_detalle, id_producto, cantidad, subtotal):
        self.cursor.execute("""
            INSERT INTO Detalle_Pedido (ID_Pedido, num_Detalle, ID_Productos, cantidad_pares, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_pedido, num_detalle, id_producto, cantidad, subtotal))
        
        self.cursor.execute("""
            UPDATE Productos SET stockActual = stockActual - %s WHERE ID_Productos = %s
        """, (cantidad, id_producto))
        self.conexion.commit()

    def agregar_detalle_y_actualizar_stock(self, id_pedido, detalles):
        for i, detalle in enumerate(detalles, start = 1):
            id_producto, cantidad, subtotal = detalle #desempaqueta la lista de tuplas ("detalles", que en la vista esta como productos_selecionados), Cada valor dentro de detalle se asigna a la variable correspondiente en orden.
            self.agregar_detalle(id_pedido, i, id_producto, cantidad, subtotal) 

    #Modulos para ver pedidos
    def obtener_datos_pedido(self):
        self.cursor.execute("")
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()