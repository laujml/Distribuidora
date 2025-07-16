import mysql.connector
from mysql.connector import Error

class ClienteModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            database='distribuidora',
            user='root',
            password='1234'
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        sql = "INSERT INTO Cliente (ID_Cliente, Nombre, Correo, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (id_cliente, nombre, correo, telefono, direccion))
        self.conn.commit()

    def buscar_cliente(self, id_cliente):
        sql = "SELECT * FROM Cliente WHERE ID_Cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        return self.cursor.fetchone()

    def actualizar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        sql = "UPDATE Cliente SET Nombre=%s, Correo=%s, Telefono=%s, Direccion=%s WHERE ID_Cliente=%s"
        self.cursor.execute(sql, (nombre, correo, telefono, direccion, id_cliente))
        self.conn.commit()

    def eliminar_cliente(self, id_cliente):
        sql = "DELETE FROM Cliente WHERE ID_Cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close() 