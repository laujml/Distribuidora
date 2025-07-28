from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Reporte.vista_reportes import ReportesView
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Controlador.Reporte.controlador_reportes import ReportesController
import sys

def main():
    app = QApplication(sys.argv)
    
    # Crear el stack primero
    stack = QStackedWidget()
    
    # Crear la vista de reportes
    reportes_view = ReportesView()
    
    # Crear el controlador con la vista y el stack
    controller = ReportesController(reportes_view, stack)
    
    # Crear la pantalla de selección después del controlador
    seleccion = PantallaSeleccion(stack, controller)
    
    # Agregar widgets al stack
    stack.addWidget(seleccion)  # Índice 0
    stack.addWidget(reportes_view)  # Índice 1
    
    # Mostrar la pantalla de selección primero
    stack.setCurrentIndex(0)
    stack.resize(800, 600)
    stack.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
