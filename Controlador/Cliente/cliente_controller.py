from Modelo.cliente_model import ClienteModel

class ClienteController:
    def __init__(self):
        # init model
        self.model = ClienteModel()

    def agregar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        # validar campos
        if not all([id_cliente, nombre, correo, telefono, direccion]):
            return False, "Todos los campos son obligatorios."
        if not id_cliente.isdigit():
            return False, "El ID ingresado es incorrecto. No se permiten letras, solo números."
        # verificar si existe
        if self.model.buscar_cliente(id_cliente):
            return False, "El ID ya existe."
        # agregar cliente
        self.model.agregar_cliente(id_cliente, nombre, correo, telefono, direccion)
        return True, "Cliente agregado exitosamente."

    def buscar_cliente(self, id_cliente):
        # validar id
        if not id_cliente:
            return False, "Ingrese el ID a buscar.", None
        if not id_cliente.isdigit():
            return False, "El ID ingresado es incorrecto. No se permiten letras, solo números.", None
        # buscar cliente
        cliente = self.model.buscar_cliente(id_cliente)
        if cliente:
            return True, "Cliente encontrado.", cliente
        else:
            return False, "No se encontró el cliente.", None

    def actualizar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        # validar campos
        if not all([id_cliente, nombre, correo, telefono, direccion]):
            return False, "Todos los campos son obligatorios."
        if not id_cliente.isdigit():
            return False, "El ID ingresado es incorrecto. No se permiten letras, solo números."
        # verificar si existe
        if not self.model.buscar_cliente(id_cliente):
            return False, "El cliente no existe."
        # actualizar cliente
        self.model.actualizar_cliente(id_cliente, nombre, correo, telefono, direccion)
        return True, "Cliente actualizado exitosamente."

    def eliminar_cliente(self, id_cliente):
        # validar id
        if not id_cliente:
            return False, "Ingrese el ID a eliminar."
        if not id_cliente.isdigit():
            return False, "El ID ingresado es incorrecto. No se permiten letras, solo números."
        # verificar si existe
        if not self.model.buscar_cliente(id_cliente):
            return False, "El cliente no existe."
        # eliminar cliente
        self.model.eliminar_cliente(id_cliente)
        return True, "Cliente eliminado exitosamente."

    def close(self):
        # cerrar conexion
        self.model.close()
