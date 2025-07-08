import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from views.principal_view import VentanaPrincipalProveedor
from views.proveedor_view import BaseProveedorVentana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    stacked_widget.setStyleSheet("background-color: #4d5a62;")

    ventana_inicio = VentanaPrincipalProveedor(stacked_widget)
    ventana_agregar = BaseProveedorVentana(stacked_widget, "Agregar Proveedor", "guardar", "Guardar")
    ventana_eliminar = BaseProveedorVentana(stacked_widget, "Eliminar Proveedor", "eliminar", "Eliminar")
    ventana_actualizar = BaseProveedorVentana(stacked_widget, "Actualizar Proveedor", "actualizar", "Actualizar")
    ventana_buscar = BaseProveedorVentana(stacked_widget, "Buscar Proveedor", "buscar", "Buscar")

    stacked_widget.addWidget(ventana_inicio)
    stacked_widget.addWidget(ventana_agregar)
    stacked_widget.addWidget(ventana_eliminar)
    stacked_widget.addWidget(ventana_actualizar)
    stacked_widget.addWidget(ventana_buscar)

    stacked_widget.setFixedSize(750, 700)
    stacked_widget.show()
    sys.exit(app.exec())
