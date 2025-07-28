# imports
from PyQt6.QtWidgets import QApplication
import sys
from Vista.Cliente.buscar_clientes import BuscarClientes  # Importar la clase padre

class BuscarProveedores(BuscarClientes):
    def __init__(self, controller, regresar_callback=None):
        # Llamar al constructor padre
        super().__init__(controller, regresar_callback)
        # Solo cambiar el título de la ventana
        self.setWindowTitle("Buscar proveedores")

    def get_labels(self):
        """Sobrescribe los labels para proveedores"""
        return ["Identificación", "Proveedor", "Contacto", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Sobrescribe el título de la ventana"""
        return "Buscar proveedores"

    def get_texto_boton_otro(self):
        """Sobrescribe el texto del botón 'otro'"""
        return "Buscar otro proveedor"

    def buscar_item(self):
        """Sobrescribe la búsqueda para proveedores"""
        return self.buscar_proveedor()

    def buscar_proveedor(self):
        """Implementación específica para buscar proveedores"""
        id_proveedor = self.campos["Identificación"].text().strip()
        if not id_proveedor.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        ok, msg, proveedor = self.controller.buscar_proveedor(id_proveedor)
        self.mostrar_popup(msg, ok)
        if ok and proveedor:
            # llenar campos
            self.campos["Proveedor"].setText(proveedor["Proveedor"])
            self.campos["Contacto"].setText(proveedor["P_Contacto"])
            self.campos["Correo"].setText(proveedor["Correo"])
            self.campos["Telefono"].setText(proveedor["Telefono"])
            self.campos["Direccion"].setText(proveedor["Direccion_Proveedor"] or "")
        else:
            self.limpiar_campos()
            self.campos["Identificación"].setText(id_proveedor)
