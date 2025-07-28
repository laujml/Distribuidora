# imports
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from Vista.Cliente.eliminar_clientes import EliminarClientes  # Importar la clase padre

class EliminarProveedores(EliminarClientes):
    def __init__(self, controller, regresar_callback=None):
        # Llamar al constructor padre
        super().__init__(controller, regresar_callback)
        # Solo cambiar el título de la ventana
        self.setWindowTitle("Eliminar proveedores")

    def get_labels(self):
        """Sobrescribe los labels para proveedores"""
        return ["Identificación", "Proveedor", "Contacto", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Sobrescribe el título de la ventana"""
        return "Eliminar proveedores"

    def get_texto_boton_otro(self):
        """Sobrescribe el texto del botón 'otro'"""
        return "Eliminar otro proveedor"

    def get_mensaje_confirmacion(self, id_item):
        """Sobrescribe el mensaje de confirmación"""
        return f"¿Seguro que deseas eliminar el proveedor con ID {id_item}?"

    def buscar_item(self):
        """Sobrescribe la búsqueda para proveedores"""
        return self.buscar_proveedor()

    def eliminar_item(self):
        """Sobrescribe la eliminación para proveedores"""
        return self.eliminar_proveedor()

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

    def eliminar_proveedor(self):
        """Implementación específica para eliminar proveedores"""
        id_proveedor = self.campos["Identificación"].text().strip()
        if not id_proveedor.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        # confirmar
        confirm = QMessageBox.question(self, "Confirmar eliminación", self.get_mensaje_confirmacion(id_proveedor), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.eliminar_proveedor(id_proveedor)
            self.mostrar_popup(msg, ok)

if __name__ == "__main__":
    # main
    app = QApplication(sys.argv)
    ventana = EliminarProveedores(None)  # controller será None para prueba
    ventana.show()
    sys.exit(app.exec())
