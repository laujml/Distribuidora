# imports
from PyQt6.QtWidgets import QMessageBox, QApplication
import sys
from Vista.Cliente.actualizar_clientes import ActualizarClientes  # Importar la clase padre

class ActualizarProveedores(ActualizarClientes):
    def __init__(self, controller, regresar_callback=None):
        # Llamar al constructor padre
        super().__init__(controller, regresar_callback)
        # Solo cambiar el título de la ventana
        self.setWindowTitle("Actualizar proveedores")

    def get_labels(self):
        """Sobrescribe los labels para proveedores"""
        return ["Identificación", "Proveedor", "Contacto", "Correo", "Telefono", "Direccion"]

    def get_titulo_ventana(self):
        """Sobrescribe el título de la ventana"""
        return "Actualizar proveedores"

    def get_texto_boton_otro(self):
        """Sobrescribe el texto del botón 'otro'"""
        return "Actualizar otro proveedor"

    def get_mensaje_confirmacion(self, id_item):
        """Sobrescribe el mensaje de confirmación"""
        return f"¿Seguro que deseas actualizar el proveedor con ID {id_item}?"

    def buscar_item(self):
        """Sobrescribe la búsqueda para proveedores"""
        id_proveedor = self.campos["Identificación"].text().strip()
        if not id_proveedor.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        
        ok, msg, proveedor = self.controller.buscar_proveedor(id_proveedor)
        self.mostrar_popup(msg, ok)
        
        if ok and proveedor:
            # Llenar campos con datos del proveedor
            self.campos["Proveedor"].setText(proveedor["Proveedor"])
            self.campos["Contacto"].setText(proveedor["P_Contacto"])
            self.campos["Correo"].setText(proveedor["Correo"])
            self.campos["Telefono"].setText(proveedor["Telefono"])
            self.campos["Direccion"].setText(proveedor["Direccion"] or "")
        else:
            self.limpiar_campos()
            self.campos["Identificación"].setText(id_proveedor)

    def actualizar_item(self):
        """Sobrescribe la actualización para proveedores"""
        # Obtener datos
        id_proveedor = self.campos["Identificación"].text().strip()
        if not id_proveedor.isdigit():
            self.mostrar_popup("El ID ingresado es incorrecto. No se permiten letras, solo números.", False)
            return
        
        proveedor = self.campos["Proveedor"].text().strip()
        p_contacto = self.campos["Contacto"].text().strip()
        correo = self.campos["Correo"].text().strip()
        telefono = self.campos["Telefono"].text().strip()
        direccion = self.campos["Direccion"].text().strip()
        
        # Confirmar actualización
        confirm = QMessageBox.question(
            self, 
            "Confirmar actualización", 
            self.get_mensaje_confirmacion(id_proveedor), 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self.controller.actualizar_proveedor(
                id_proveedor, proveedor, p_contacto, correo, telefono, direccion
            )
            self.mostrar_popup(msg, ok)

    # Alias para mantener compatibilidad con nombres específicos
    def buscar_proveedor(self):
        return self.buscar_item()
    
    def actualizar_proveedor(self):
        return self.actualizar_item()

if __name__ == "__main__":
    # main
    app = QApplication(sys.argv)
    ventana = ActualizarProveedores(None)  # controller será None para prueba
    ventana.show()
    sys.exit(app.exec())
