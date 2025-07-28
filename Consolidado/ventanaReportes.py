from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Reporte.vista_reportes import ReportesView
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Controlador.Reporte.controlador_reportes import ReportesController
import sys

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    
   
    reportes_view = ReportesView()
    controller = ReportesController(reportes_view, stack)
    
  
    seleccion = PantallaSeleccion(stack, controller)
    
   
    stack.addWidget(seleccion)
    stack.addWidget(reportes_view)
    
   
    stack.setCurrentIndex(0)
    stack.resize(800, 600)
    stack.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
