from mysql.connector import Error
from Modelo.db_config import conectar

class ProveedorModel:
    def __init__(self):
        # init connection
        self.conn = conectar()
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        # insert query
        sql = "INSERT INTO Proveedor (ID_Proveedor, Proveedor, P_Contacto, Correo, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor))
        self.conn.commit()

    def buscar_proveedor(self, id_proveedor):
        # select query
        sql = "SELECT * FROM Proveedor WHERE ID_Proveedor = %s"
        self.cursor.execute(sql, (id_proveedor,))
        return self.cursor.fetchone()

    def actualizar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        # update query
        sql = "UPDATE Proveedor SET Proveedor=%s, P_Contacto=%s, Correo=%s, Telefono=%s, Direccion=%s WHERE ID_Proveedor=%s"
        self.cursor.execute(sql, (proveedor, p_contacto, correo, telefono, direccion_proveedor, id_proveedor))
        self.conn.commit()

    def eliminar_proveedor(self, id_proveedor):
        # delete query
        sql = "DELETE FROM Proveedor WHERE ID_Proveedor = %s"
        self.cursor.execute(sql, (id_proveedor,))
        self.conn.commit()

    def close(self):
        # cerrar conexion
        self.cursor.close()
        self.conn.close()
