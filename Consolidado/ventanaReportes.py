# reportes_main.py - Archivo separado o función en tu main principal

from PyQt6.QtWidgets import QStackedWidget
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Vista.Reporte.vista_reportes import ReportesView
from Controlador.Reporte.controlador_reportes import ReportesController
from Modelo.db_config import conectar

def crear_modulo_reportes():
    """
    Función que crea y configura todo el módulo de reportes
    Retorna el widget principal listo para usar
    """
    # Crear el stack principal de reportes
    stack = QStackedWidget()
    
    # Crear vista y controlador
    reportes_view = ReportesView()
    reportes_controller = ReportesController(reportes_view, conectar)
    
    # Asignar el stack al controlador para navegación
    reportes_controller.set_stack(stack)
    
    # Crear pantalla de selección
    seleccion = PantallaSeleccion(stack)
    
    # Agregar widgets al stack
    stack.addWidget(seleccion)      # Índice 0
    stack.addWidget(reportes_view)  # Índice 1
    
    # Conectar señales de la pantalla de selección
    seleccion.ir_a_semanal.connect(lambda: reportes_controller.mostrar_reporte("Semanal"))
    seleccion.ir_a_mensual.connect(lambda: reportes_controller.mostrar_reporte("Mensual"))
    
    # Conectar señal del botón regresar
    reportes_view.regresar_clicked.connect(lambda: stack.setCurrentIndex(0))
    
    # Mostrar pantalla inicial
    stack.setCurrentIndex(0)
    
    # Agregar referencias para limpieza posterior si es necesario
    stack.reportes_controller = reportes_controller  # Para poder cerrar conexiones después
    stack.reportes_view = reportes_view
    stack.seleccion = seleccion
    
    return stack

def main_reportes_standalone():
    """Función para ejecutar reportes como aplicación independiente"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Crear módulo de reportes
    reportes_widget = crear_modulo_reportes()
    
    # Mostrar
    reportes_widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main_reportes_standalone()
