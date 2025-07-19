from Modelo.db_config import conectar

class ClienteModel:
    def __init__(self):
        # init connection
        self.conn = conectar()
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        # insert query
        sql = "INSERT INTO Cliente (ID_Cliente, Nombre, Correo, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (id_cliente, nombre, correo, telefono, direccion))
        self.conn.commit()

    def buscar_cliente(self, id_cliente):
        # select query
        sql = "SELECT * FROM Cliente WHERE ID_Cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        return self.cursor.fetchone()

    def actualizar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        # update query
        sql = "UPDATE Cliente SET Nombre=%s, Correo=%s, Telefono=%s, Direccion=%s WHERE ID_Cliente=%s"
        self.cursor.execute(sql, (nombre, correo, telefono, direccion, id_cliente))
        self.conn.commit()

    def eliminar_cliente(self, id_cliente):
        # delete query
        sql = "DELETE FROM Cliente WHERE ID_Cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        self.conn.commit()

    def close(self):
        # cerrar conexion
        self.cursor.close()
        self.conn.close()
