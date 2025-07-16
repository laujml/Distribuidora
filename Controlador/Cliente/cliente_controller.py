from Modelo.Cliente.cliente_model import ClienteModel

class ClienteController:
    def __init__(self):
        self.model = ClienteModel()

    def agregar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        if not all([id_cliente, nombre, correo, telefono, direccion]):
            return False, "Todos los campos son obligatorios."
        if self.model.buscar_cliente(id_cliente):
            return False, "El ID ya existe."
        self.model.agregar_cliente(id_cliente, nombre, correo, telefono, direccion)
        return True, "Cliente agregado exitosamente."

    def buscar_cliente(self, id_cliente):
        if not id_cliente:
            return False, "Ingrese el ID a buscar.", None
        cliente = self.model.buscar_cliente(id_cliente)
        if cliente:
            return True, "Cliente encontrado.", cliente
        else:
            return False, "No se encontró el cliente.", None

    def actualizar_cliente(self, id_cliente, nombre, correo, telefono, direccion):
        if not all([id_cliente, nombre, correo, telefono, direccion]):
            return False, "Todos los campos son obligatorios."
        if not self.model.buscar_cliente(id_cliente):
            return False, "El cliente no existe."
        self.model.actualizar_cliente(id_cliente, nombre, correo, telefono, direccion)
        return True, "Cliente actualizado exitosamente."

    def eliminar_cliente(self, id_cliente):
        if not id_cliente:
            return False, "Ingrese el ID a eliminar."
        if not self.model.buscar_cliente(id_cliente):
            return False, "El cliente no existe."
        self.model.eliminar_cliente(id_cliente)
        return True, "Cliente eliminado exitosamente."

    def close(self):
        self.model.close() 
