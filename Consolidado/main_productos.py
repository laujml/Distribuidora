from PyQt6.QtWidgets import QStackedWidget
from Consolidado.ventanaProductos import (
    VentanaProductosPrincipal, BaseProductoVentana, VerProductosTabla
)

def crear_sistema_productos():
    stack_productos = QStackedWidget()

    ventana_inicio = VentanaProductosPrincipal(stack_productos)
    ventana_agregar = BaseProductoVentana(stack_productos, "Agregar Producto", "guardar", "Guardar", mostrar_buscar=False)
    ventana_eliminar = BaseProductoVentana(stack_productos, "Eliminar Producto", "eliminar", "Eliminar")
    ventana_ver = VerProductosTabla(stack_productos)
    ventana_actualizar = BaseProductoVentana(stack_productos, "Actualizar Producto", "actualizar", "Actualizar")

    stack_productos.addWidget(ventana_inicio)
    stack_productos.addWidget(ventana_agregar)
    stack_productos.addWidget(ventana_eliminar)
    stack_productos.addWidget(ventana_ver)
    stack_productos.addWidget(ventana_actualizar)

    return stack_productos
