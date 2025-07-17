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

    def obtener_estado(self):
        self.cursor.execute("SELECT id_estado, estado FROM Estado e;")
        return self.cursor.fetchall()
    
    def crear_pedido(self, id_cliente, total, estado, pendiente_pagar, plazo_dias):
        fecha_actual = datetime.now()
        self.cursor.execute("""
            INSERT INTO Pedido (ID_Cliente, fecha_hora, total, id_estado, pendiente_pagar, plazo_dias)
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
    
    def obtener_stock_producto(self, id_producto):
        self.cursor.execute("SELECT stockActual FROM Productos WHERE ID_Productos = %s", (id_producto,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0
        
    #Modelos para ver pedidos
    def obtener_datos_pedido(self):
        cursor_dict = self.conexion.cursor(dictionary=True)
        consulta = """
            SELECT p.fecha_hora, p.ID_Pedido, p.ID_Cliente, c.Nombre, c.Telefono, 
                ps.ID_Productos, ps.descripcion, ps.precio, dp.cantidad_pares, dp.subtotal, 
                p.total, e.estado AS estado_nombre, p.pendiente_pagar, p.plazo_dias
            FROM Pedido p
            INNER JOIN Cliente c ON p.ID_Cliente = c.ID_Cliente
            INNER JOIN detalle_pedido dp ON p.ID_Pedido = dp.ID_Pedido
            INNER JOIN Productos ps ON dp.ID_Productos = ps.ID_Productos
            INNER JOIN Estado e ON p.id_estado = e.id_estado
            ORDER BY p.fecha_hora desc
        """
        cursor_dict.execute(consulta)
        filas = cursor_dict.fetchall()

        pedidos = {}
        for fila in filas:
            id_pedido = fila["ID_Pedido"]
            if id_pedido not in pedidos:
                pedidos[id_pedido] = {
                    "fecha": fila["fecha_hora"],
                    "numero": id_pedido,
                    "cliente_id": fila["ID_Cliente"],
                    "nombre": fila["Nombre"],
                    "telefono": fila["Telefono"],
                    "total": fila["total"],
                    "estado": fila["estado_nombre"],
                    "pendiente_pagar": fila["pendiente_pagar"],
                    "plazo_dias": fila["plazo_dias"],
                    "productos": []
                }
            pedidos[id_pedido]["productos"].append({
                "codigo": fila["ID_Productos"],
                "nombre": fila["descripcion"],
                "precio": fila["precio"],
                "cantidad": fila["cantidad_pares"],
                "subtotal": fila["subtotal"]
            })

        cursor_dict.close()
        return list(pedidos.values())
    
    def eliminar_pedido(self, id_pedido):
        self.cursor.execute("""
            SELECT ID_Productos, cantidad_pares 
            FROM Detalle_Pedido 
            WHERE ID_Pedido = %s
        """, (id_pedido,))
        detalles = self.cursor.fetchall()

        #Devolver stock
        for fila in detalles:
            id_producto = fila[0]
            cantidad = fila[1]
            self.cursor.execute("""
                UPDATE Productos SET stockActual = stockActual + %s 
                WHERE ID_Productos = %s
            """, (cantidad, id_producto))

        #Eliminar detalles y pedido (la base lo hace automaticamnete, pero lo hago aqui por mas seguridad)
        self.cursor.execute("DELETE FROM Detalle_Pedido WHERE ID_Pedido = %s", (id_pedido,))
        self.cursor.execute("DELETE FROM Pedido WHERE ID_Pedido = %s", (id_pedido,))
        
        self.conexion.commit()

    #Consultas para editar los pedidos
    def actualizar_pedido(self, id_pedido, cliente_id, total, estado, pendiente_pagar, plazo_dias, detalles):
        try:
            # Primero obtener los productos y cantidades actuales para devolver stock
            self.cursor.execute("SELECT ID_Productos, cantidad_pares FROM Detalle_Pedido WHERE ID_Pedido = %s", (id_pedido,))
            detalles_anteriores = self.cursor.fetchall()
            
            # Devolver stock actual
            for id_producto, cantidad in detalles_anteriores:
                self.cursor.execute("UPDATE Productos SET stockActual = stockActual + %s WHERE ID_Productos = %s", (cantidad, id_producto))

            # Actualizar tabla Pedido
            self.cursor.execute("""
                UPDATE Pedido SET ID_Cliente = %s, total = %s, estado = %s, pendiente_pagar = %s, plazo_dias = %s
                WHERE ID_Pedido = %s
            """, (cliente_id, total, estado, pendiente_pagar, plazo_dias, id_pedido))

            # Eliminar detalles anteriores
            self.cursor.execute("DELETE FROM Detalle_Pedido WHERE ID_Pedido = %s", (id_pedido,))

            # Insertar nuevos detalles y descontar stock
            for i, detalle in enumerate(detalles, start=1):
                id_producto, cantidad, subtotal = detalle  # cada detalle: (id_producto, cantidad, subtotal)
                self.cursor.execute("""
                    INSERT INTO Detalle_Pedido (ID_Pedido, num_Detalle, ID_Productos, cantidad_pares, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_pedido, i, id_producto, cantidad, subtotal))
                self.cursor.execute("""
                    UPDATE Productos SET stockActual = stockActual - %s WHERE ID_Productos = %s
                """, (cantidad, id_producto))

            self.conexion.commit()
            return True
        except Exception as e:
            print("Error actualizando pedido:", e)
            self.conexion.rollback()
            return False

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()
