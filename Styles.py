from PyQt6.QtWidgets import QApplication, QListWidget, QWidget

class Styles:
    """Estilos generales reutilizables para la aplicación."""

    PRIMARY_TEXT = "#4d5a62"
    BACKGROUND = "#4d5a62"
    WHITE = "#ffffff"
    BORDER = "#dee2e6"
    HIGHLIGHT = "#f5f7fa"
    MENU_ANCHO = 130
    PANEL_PEDIDOS_ANCHO = 120

    @staticmethod
    def aplicar_estilo_global(widget_raiz: QWidget, menu: QListWidget):
        """
        Aplica estilos a toda la aplicación y al menú lateral.
        """
        # Configura el menú
        menu.setObjectName("menuLateral")
        menu.setFixedWidth(Styles.MENU_ANCHO)

        # Aplica hoja de estilo al widget raíz
        widget_raiz.setStyleSheet(Styles.get_stylesheet())
        
    def panel_izquierdo(panel: QWidget):
        panel.setObjectName("panelIzquierdo")
        panel.setFixedWidth(Styles.PANEL_PEDIDOS_ANCHO) 

    @staticmethod
    def get_stylesheet():
        return f"""
            /* Fondo global */
            QWidget {{
                background-color: {Styles.BACKGROUND};
                color: #f0f0f0;
                font-family: 'Poppins', sans-serif;
                font-size: 12px;
            }}

            QLabel {{
                color: #f0f0f0;
                background-color: transparent;
            }}

            QLabel#primerLabel{{
                color: #f0f0f0;
                background-color: transparent;
                font-size: 25px;
                font-weight: bold;
            }}

            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,QDateEdit {{
                background-color: {Styles.WHITE};
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 4px 8px;
                border-radius: 6px;
            }}

            QTableWidget {{
                background-color: {Styles.WHITE};
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                gridline-color: {Styles.BORDER};
                font-size: 12px;
            }}

            QTableWidget::item:selected {{
                background-color: {Styles.HIGHLIGHT};
                color: {Styles.PRIMARY_TEXT};
            }}

            QHeaderView::section {{
                background-color: {Styles.HIGHLIGHT};
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 4px;
                font-weight: bold;
            }}

            QPushButton {{
                background: #ffffff;
                color: {Styles.PRIMARY_TEXT};
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 11px;
                border: 1px solid {Styles.PRIMARY_TEXT};
                min-height: 26px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #f0f0f0;
            }}

            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}

            /* Solo el panel lateral izquierdo */
            QWidget#panelIzquierdo {{
                background-color: {Styles.WHITE};
                color: {Styles.PRIMARY_TEXT};
                border-right: 1px solid {Styles.BORDER};
            }}

            QListWidget#panelIzquierdo {{
            background-color: white;
            color: #4d5a62;
            border: 1px solid #dee2e6;
            }}

            QListWidget#menuLateral {{
            background-color: white;
            color: #4d5a62;  /* El azul oscuro que usas en el resto */
            border: none;
            font-weight: bold;
            }}

            QListWidget#menuLateral::item {{
                padding: 6px 12px;
            }}

            QListWidget#menuLateral::item:selected {{
                background-color: #d0e1ff;  /* un azul clarito para el item seleccionado */
                color: #1a2b4c;  /* un azul más oscuro para el texto seleccionado */
            }}

            QWidget#contenedorTabla {{
            background-color: white;
            }}

            /* Fondo del desplegable (la lista que se abre) */
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                selection-background-color: {Styles.HIGHLIGHT};
                selection-color: {Styles.PRIMARY_TEXT};
            }}

            /* Estilos corregidos para QSpinBox y QDoubleSpinBox */
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                height: 12px;
                border-left: 1px solid {Styles.BORDER};
                border-bottom: 1px solid {Styles.BORDER};
                background-color: {Styles.WHITE};
                border-top-right-radius: 4px;
            }}

            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                height: 12px;
                border-left: 1px solid {Styles.BORDER};
                border-top: 1px solid {Styles.BORDER};
                background-color: {Styles.WHITE};
                border-bottom-right-radius: 4px;
            }}

            /* Hover para los botones */
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
                background-color: #e6f3ff;
            }}

            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
                background-color: #e6f3ff;
            }}

            /* Pressed para los botones */
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
                background-color: #cce7ff;
            }}

            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
                background-color: #cce7ff;
            }}

            /* Flechas triangulares más pequeñas y precisas */
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                width: 0;
                height: 0;
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-bottom: 3px solid {Styles.PRIMARY_TEXT};
            }}

            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                width: 0;
                height: 0;
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-top: 3px solid {Styles.PRIMARY_TEXT};
            }}

            /* Flechas cuando están presionadas - más pequeñas */
            QSpinBox::up-arrow:pressed, QDoubleSpinBox::up-arrow:pressed {{
                width: 0;
                height: 0;
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-bottom: 3px solid #2a3a4a;
            }}

            QSpinBox::down-arrow:pressed, QDoubleSpinBox::down-arrow:pressed {{
                width: 0;
                height: 0;
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-top: 3px solid #2a3a4a;
            }}
        """
