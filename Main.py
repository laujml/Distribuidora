import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from pantalla_seleccion import PantallaSeleccion
from vista_reportes import ReportesView
from controlador_reportes import ReportesController
import os

def main():
    app = QApplication(sys.argv)

    # Create the stacked widget
    stack = QStackedWidget()

    # Initialize screens
    seleccion = PantallaSeleccion(stack)
    reportes_view = ReportesView()
    reportes_controller = ReportesController(reportes_view)

    # Add screens to the stack
    stack.addWidget(seleccion)        # Index 0
    stack.addWidget(reportes_view)    # Index 1

    # Connect signals from PantallaSeleccion to ReportesController
    seleccion.ir_a_semanal.connect(lambda: reportes_controller.mostrar_reporte("Semanal"))
    seleccion.ir_a_mensual.connect(lambda: reportes_controller.mostrar_reporte("Mensual"))

    # Set initial screen
    stack.setCurrentIndex(0)

    # Show the application
    stack.setWindowTitle("Distribuidora App")
    stack.resize(1000, 800)
    stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    # Ensure the logo file exists
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
    if not os.path.exists(logo_path):
        print(f"Warning: Logo file not found at {logo_path}")
    main()