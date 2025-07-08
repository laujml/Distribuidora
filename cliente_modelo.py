import mysql.connector

class ClienteModelo:
    def conectar_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="distribuidora"
        )

    def guardar_cliente(self, datos):
        conn = self.conectar_db()
        cursor = conn.cursor()
        sql = "INSERT INTO cliente (id_cliente, nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, datos)
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar_cliente(self, id_cliente):
        conn = self.conectar_db()
        cursor = conn.cursor()
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        eliminado = cursor.rowcount
        cursor.close()
        conn.close()
        return eliminado

    def actualizar_cliente(self, datos):
        conn = self.conectar_db()
        cursor = conn.cursor()
        sql = "UPDATE cliente SET nombre=%s, correo=%s, telefono=%s, direccion=%s WHERE id_cliente=%s"
        cursor.execute(sql, datos)
        conn.commit()
        actualizado = cursor.rowcount
        cursor.close()
        conn.close()
        return actualizado

    def buscar_cliente(self, condiciones, valores):
        conn = self.conectar_db()
        cursor = conn.cursor()
        sql = f"SELECT id_cliente, nombre, correo, telefono, direccion FROM cliente WHERE {' AND '.join(condiciones)}"
        cursor.execute(sql, tuple(valores))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado
