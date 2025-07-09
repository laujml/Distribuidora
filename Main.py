import sys
from PyQt6.QtWidgets import QApplication
from controlador_reportes import ReportesController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = ReportesController()
    controller.show()
    sys.exit(app.exec())