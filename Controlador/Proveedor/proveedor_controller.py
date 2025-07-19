from Modelo.proveedor_model import ProveedorModel

class ProveedorController:
    def __init__(self):
        # init model
        self.model = ProveedorModel()

    def agregar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        # validar campos
        if not all([id_proveedor, proveedor, p_contacto, correo, telefono]):
            return False, "Los campos ID, Proveedor, Contacto, Correo y Teléfono son obligatorios."
        # verificar si existe
        if self.model.buscar_proveedor(id_proveedor):
            return False, "El ID ya existe."
        # agregar proveedor
        self.model.agregar_proveedor(id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
        return True, "Proveedor agregado exitosamente."

    def buscar_proveedor(self, id_proveedor):
        # validar id
        if not id_proveedor:
            return False, "Ingrese el ID a buscar.", None
        # buscar proveedor
        proveedor = self.model.buscar_proveedor(id_proveedor)
        if proveedor:
            return True, "Proveedor encontrado.", proveedor
        else:
            return False, "No se encontró el proveedor.", None

    def actualizar_proveedor(self, id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor):
        # validar campos
        if not all([id_proveedor, proveedor, p_contacto, correo, telefono]):
            return False, "Los campos ID, Proveedor, Contacto, Correo y Teléfono son obligatorios."
        # verificar si existe
        if not self.model.buscar_proveedor(id_proveedor):
            return False, "El proveedor no existe."
        # actualizar proveedor
        self.model.actualizar_proveedor(id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
        return True, "Proveedor actualizado exitosamente."

    def eliminar_proveedor(self, id_proveedor):
        # validar id
        if not id_proveedor:
            return False, "Ingrese el ID a eliminar."
        # verificar si existe
        if not self.model.buscar_proveedor(id_proveedor):
            return False, "El proveedor no existe."
        # eliminar proveedor
        self.model.eliminar_proveedor(id_proveedor)
        return True, "Proveedor eliminado exitosamente."

    def close(self):
        # cerrar conexion
        self.model.close()
