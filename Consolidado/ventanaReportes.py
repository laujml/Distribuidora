import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Vista.Reporte.vista_reportes import ReportesView
from Controlador.Reporte.controlador_reportes import ReportesController

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    
    # Crear vista y controlador
    reportes_view = ReportesView()
    reportes_controller = ReportesController(reportes_view)  # Pasar la vista
    
    # Crear pantalla de selección
    seleccion = PantallaSeleccion(stack)
    
    # Agregar al stack
    stack.addWidget(seleccion)
    stack.addWidget(reportes_view)
    
    # Conectar señales
    seleccion.ir_a_semanal.connect(lambda: reportes_controller.mostrar_reporte("Semanal"))
    seleccion.ir_a_mensual.connect(lambda: reportes_controller.mostrar_reporte("Mensual"))
    
    # Mostrar
    stack.setCurrentIndex(0)
    stack.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
