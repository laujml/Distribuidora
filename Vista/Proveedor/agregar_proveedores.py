# imports
from PyQt6.QtWidgets import QApplication
import sys
from Vista.Cliente.agregar_clientes import AgregarClientes  # Importar la clase padre

class AgregarProveedores(AgregarClientes):
    def __init__(self, controller, regresar_callback=None):
        # Llamar al constructor padre
        super().__init__(controller, regresar_callback)
        # Solo cambiar el título de la ventana
        self.setWindowTitle("Agregar proveedores")

    def get_labels(self):
        """Sobrescribe los labels para proveedores"""
        return ["Identificación", "Proveedor", "Contacto", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Sobrescribe el título de la ventana"""
        return "Agregar proveedores"

    def get_texto_boton_otro(self):
        """Sobrescribe el texto del botón 'otro'"""
        return "Agregar otro proveedor"

    def guardar_item(self):
        """Sobrescribe el guardado para proveedores"""
        return self.guardar_proveedor()

    def guardar_proveedor(self):
        """Implementación específica para guardar proveedores"""
        # obtener datos
        id_proveedor = self.campos["Identificación"].text().strip()
        if not id_proveedor.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        proveedor = self.campos["Proveedor"].text().strip()
        p_contacto = self.campos["Contacto"].text().strip()
        correo = self.campos["Correo"].text().strip()
        telefono = self.campos["Telefono"].text().strip()
        direccion = self.campos["Direccion"].text().strip()
        ok, msg = self.controller.agregar_proveedor(id_proveedor, proveedor, p_contacto, correo, telefono, direccion)
        self.mostrar_popup(msg, ok)
