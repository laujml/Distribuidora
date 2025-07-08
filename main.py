import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from vista.pantalla_principal import VentanaPrincipal
from vista.base_ventana import BaseVentana

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    stacked_widget.setStyleSheet("background-color: #4d5a62;")

    ventana_inicio = VentanaPrincipal(stacked_widget)
    ventana_agregar = BaseVentana(stacked_widget, "Agregar Cliente", "guardar", "Guardar", mostrar_buscar=False)
    ventana_eliminar = BaseVentana(stacked_widget, "Eliminar Cliente", "eliminar", "Eliminar")
    ventana_actualizar = BaseVentana(stacked_widget, "Actualizar Cliente", "actualizar", "Actualizar")
    ventana_buscar = BaseVentana(stacked_widget, "Buscar Cliente", "buscar", "Buscar", mostrar_buscar=False)

    stacked_widget.addWidget(ventana_inicio)
    stacked_widget.addWidget(ventana_agregar)
    stacked_widget.addWidget(ventana_eliminar)
    stacked_widget.addWidget(ventana_actualizar)
    stacked_widget.addWidget(ventana_buscar)

    stacked_widget.setFixedSize(750, 700)
    stacked_widget.show()
    sys.exit(app.exec())
