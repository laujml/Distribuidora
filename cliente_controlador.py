from modelo.cliente_modelo import ClienteModelo
from PyQt6.QtWidgets import QMessageBox

class ClienteControlador:
    def __init__(self):
        self.modelo = ClienteModelo()

    def ejecutar_accion(self, accion, inputs, ventana):
        if accion == "guardar":
            self.guardar(inputs, ventana)
        elif accion == "eliminar":
            self.eliminar(inputs, ventana)
        elif accion == "actualizar":
            self.actualizar(inputs, ventana)

    def guardar(self, inputs, ventana):
        datos = tuple(inputs[campo].text() for campo in ["identificación", "nombre", "correo", "telefono", "direccion"])
        if not all(datos):
            QMessageBox.warning(ventana, "Campos vacíos", "Por favor llena todos los campos.")
            return
        try:
            int(datos[0])
        except ValueError:
            QMessageBox.warning(ventana, "Error", "Identificación debe contener solo números.")
            return
        try:
            self.modelo.guardar_cliente(datos)
            QMessageBox.information(ventana, "Éxito", "Cliente guardado exitosamente.")
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"No se pudo guardar: {e}")

    def eliminar(self, inputs, ventana):
        id_cliente = inputs["identificación"].text()
        if not id_cliente:
            QMessageBox.warning(ventana, "Campo vacío", "Ingresa el ID del cliente.")
            return
        try:
            id_cliente_int = int(id_cliente)
        except ValueError:
            QMessageBox.warning(ventana, "Error", "Identificación debe contener solo números.")
            return
        try:
            eliminado = self.modelo.eliminar_cliente(id_cliente_int)
            if eliminado:
                QMessageBox.information(ventana, "Eliminado", "Cliente eliminado correctamente.")
                ventana.limpiar_campos()
            else:
                QMessageBox.warning(ventana, "No encontrado", "Cliente no existe.")
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al eliminar: {e}")

    def actualizar(self, inputs, ventana):
        datos = (
            inputs["nombre"].text(),
            inputs["correo"].text(),
            inputs["telefono"].text(),
            inputs["direccion"].text(),
            inputs["identificación"].text()
        )
        if not all(datos):
            QMessageBox.warning(ventana, "Campos vacíos", "Por favor llena todos los campos.")
            return
        try:
            int(datos[-1])
        except ValueError:
            QMessageBox.warning(ventana, "Error", "Identificación debe ser un número entero.")
            return
        try:
            actualizado = self.modelo.actualizar_cliente(datos)
            if actualizado:
                QMessageBox.information(ventana, "Actualizado", "Datos del cliente actualizados.")
            else:
                QMessageBox.warning(ventana, "No encontrado", "Cliente no existe.")
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al actualizar: {e}")

    def buscar_cliente(self, inputs, ventana):
        condiciones = []
        valores = []
        mapeo = {
            "identificación": "id_cliente",
            "nombre": "nombre",
            "correo": "correo",
            "telefono": "telefono",
            "direccion": "direccion"
        }

        for campo, db_col in mapeo.items():
            valor = inputs[campo].text().strip()
            if valor:
                if campo == "identificación":
                    try:
                        valor = int(valor)
                    except ValueError:
                        QMessageBox.warning(ventana, "Error", "Identificación debe ser un número.")
                        return
                condiciones.append(f"{db_col} = %s")
                valores.append(valor)

        if not condiciones:
            QMessageBox.warning(ventana, "Campos vacíos", "Ingresa al menos un campo para buscar.")
            return

        try:
            resultado = self.modelo.buscar_cliente(condiciones, valores)
            if resultado:
                for i, campo in enumerate(["identificación", "nombre", "correo", "telefono", "direccion"]):
                    inputs[campo].setText(str(resultado[i]))
                QMessageBox.information(ventana, "Consulta exitosa", "Cliente encontrado.")
            else:
                QMessageBox.warning(ventana, "No encontrado", "No se encontró ningún cliente.")
                ventana.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al consultar: {e}")
