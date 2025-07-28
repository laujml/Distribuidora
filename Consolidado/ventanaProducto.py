from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Producto.menuProductos import MenuPrincipalView
from Vista.Producto.formularioProducto import FormularioProductoView
from Vista.Producto.tablaProductos import TablaProductosView
from Controlador.Producto.producto_controlador import ProductoController

class AplicacionProductos:
    def __init__(self, parent=None):
        self.stacked_widget = QStackedWidget(parent)

        # Crear controlador (sin vistas aún)
        self.controlador = ProductoController()

        # Crear vistas, pasándoles el stacked_widget y controlador
        self.menu_principal = MenuPrincipalView(self.stacked_widget, self.controlador)

        self.form_guardar = FormularioProductoView(
            self.stacked_widget, "Agregar Producto", "guardar", "Guardar", self.controlador, mostrar_buscar=False
        )
        self.form_eliminar = FormularioProductoView(
            self.stacked_widget, "Eliminar Producto", "eliminar", "Eliminar", self.controlador, mostrar_buscar=True
        )
        self.form_actualizar = FormularioProductoView(
            self.stacked_widget, "Actualizar Producto", "actualizar", "Actualizar", self.controlador, mostrar_buscar=True
        )

        self.tabla_productos = TablaProductosView(self.stacked_widget, self.controlador)

        # Añadir vistas al stacked widget en el orden correcto
        self.stacked_widget.addWidget(self.menu_principal)     # índice 0
        self.stacked_widget.addWidget(self.form_guardar)       # índice 1
        self.stacked_widget.addWidget(self.form_eliminar)      # índice 2
        self.stacked_widget.addWidget(self.tabla_productos)    # índice 3
        self.stacked_widget.addWidget(self.form_actualizar)    # índice 4

        # Pasar referencias al controlador
        self.controlador.vista_menu = self.menu_principal
        self.controlador.vista_tabla = self.tabla_productos

        # Diccionario de vistas formulario para navegación dinámica
        self.controlador.vistas_formulario = {
            1: self.form_guardar,
            2: self.form_eliminar,
            4: self.form_actualizar
        }

        # Inicialmente vista_formulario = form_guardar
        self.controlador.vista_formulario = self.form_guardar

    def ejecutar(self):
        self.stacked_widget.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    aplicacion = AplicacionProductos()
    aplicacion.ejecutar()
    sys.exit(app.exec())
