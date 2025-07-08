import mysql.connector
from PyQt6.QtWidgets import QMessageBox

class ProveedorModel:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget

    def conectar_db(self):
        return mysql.connector.connect(host="localhost", user="root", password="1234", database="distribuidora")

    def guardar_proveedor(self, datos):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO proveedor (id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, datos)
            conn.commit()
            QMessageBox.information(self.parent_widget, "Éxito", "Proveedor guardado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Error", f"No se pudo guardar: {e}")

    def actualizar_proveedor(self, datos):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = """
                UPDATE proveedor SET proveedor=%s, p_contacto=%s, correo=%s, telefono=%s, direccion_proveedor=%s
                WHERE id_proveedor=%s
            """
            cursor.execute(sql, datos)
            conn.commit()
            QMessageBox.information(self.parent_widget, "Actualizado", "Datos actualizados.")
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Error", f"Error al actualizar: {e}")

    def eliminar_proveedor(self, id_proveedor):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
            conn.commit()
            QMessageBox.information(self.parent_widget, "Eliminado", "Proveedor eliminado correctamente.")
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Error", f"Error al eliminar: {e}")

    def consultar_proveedor(self, id_proveedor):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT proveedor, p_contacto, correo, telefono, direccion_proveedor FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            QMessageBox.critical(self.parent_widget, "Error", f"Error al consultar: {e}")
            return None
