from Modelo.proveedor_model import ProveedorModel

class ProveedorController:
    def __init__(self):
        self.model = ProveedorModel()

    def agregar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        if not all([id_proveedor, proveedor, p_contacto, correo, telefono]):
            return False, "Los campos ID, Proveedor, Contacto, Correo y Teléfono son obligatorios."
        if self.model.buscar_proveedor(id_proveedor):
            return False, "El ID ya existe."
        self.model.agregar_proveedor(id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
        return True, "Proveedor agregado exitosamente."

    def buscar_proveedor(self, id_proveedor):
        if not id_proveedor:
            return False, "Ingrese el ID a buscar.", None
        proveedor = self.model.buscar_proveedor(id_proveedor)
        if proveedor:
            return True, "Proveedor encontrado.", proveedor
        else:
            return False, "No se encontró el proveedor.", None

    def actualizar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        if not all([id_proveedor, proveedor, p_contacto, correo, telefono]):
            return False, "Los campos ID, Proveedor, Contacto, Correo y Teléfono son obligatorios."
        if not self.model.buscar_proveedor(id_proveedor):
            return False, "El proveedor no existe."
        self.model.actualizar_proveedor(id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
        return True, "Proveedor actualizado exitosamente."

    def eliminar_proveedor(self, id_proveedor):
        if not id_proveedor:
            return False, "Ingrese el ID a eliminar."
        if not self.model.buscar_proveedor(id_proveedor):
            return False, "El proveedor no existe."
        self.model.eliminar_proveedor(id_proveedor)
        return True, "Proveedor eliminado exitosamente."

    def close(self):
        self.model.close() 
