import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from pantalla_seleccion import PantallaSeleccion
from vista_reportes import ReportesView
from controlador_reportes import ReportesController
from db_config import conectar

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    
    # Crear vista y controlador
    reportes_view = ReportesView()
    reportes_controller = ReportesController(reportes_view, conectar)  # Pasar la función conectar
    
    # Asignar el stack al controlador para que pueda navegar
    reportes_controller.set_stack(stack)
    
    # Crear pantalla de selección
    seleccion = PantallaSeleccion(stack)
    
    # Agregar al stack
    stack.addWidget(seleccion)
    stack.addWidget(reportes_view)
    
    # Conectar señales de la pantalla de selección
    seleccion.ir_a_semanal.connect(lambda: reportes_controller.mostrar_reporte("Semanal"))
    seleccion.ir_a_mensual.connect(lambda: reportes_controller.mostrar_reporte("Mensual"))
    
    # Conectar señal del botón regresar de la vista de reportes
    reportes_view.regresar_clicked.connect(lambda: stack.setCurrentIndex(0))
    
    # Mostrar
    stack.setCurrentIndex(0)
    stack.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
