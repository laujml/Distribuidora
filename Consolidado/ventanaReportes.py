import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from Vista.Reporte.pantalla_seleccion import PantallaSeleccion
from Vista.Reporte.vista_reportes import ReportesView
from Controlador.Reporte.controlador_reportes import ReportesController
import os

def main():
    app = QApplication(sys.argv)

    
    stack = QStackedWidget()

    seleccion = PantallaSeleccion(stack)
    reportes_view = ReportesView()
    reportes_controller = ReportesController(reportes_view)

   
    stack.addWidget(seleccion)       
    stack.addWidget(reportes_view)    

    seleccion.ir_a_semanal.connect(lambda: reportes_controller.mostrar_reporte("Semanal"))
    seleccion.ir_a_mensual.connect(lambda: reportes_controller.mostrar_reporte("Mensual"))

 
    stack.setCurrentIndex(0)

    
    stack.setWindowTitle("Distribuidora App")
    stack.resize(1000, 800)
    stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
   
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    if not os.path.exists(logo_path):
        print(f"Warning: Logo file not found at {logo_path}")
    main()
