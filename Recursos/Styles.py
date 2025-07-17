from PyQt6.QtWidgets import QWidget, QListWidget

class Styles:
    PRIMARY_TEXT = "#4d5a62"
    BACKGROUND = "#4d5a62"
    WHITE = "#ffffff"
    BORDER = "#dee2e6"
    HIGHLIGHT = "#f5f7fa"
    MENU_ANCHO = 100
    PANEL_PEDIDOS_ANCHO = 120

    @staticmethod
    def global_stylesheet():
        return f"""
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

            QLabel#primerLabel {{
                font-size: 25px;
                font-weight: bold;
            }}

            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
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
                background: {Styles.WHITE};
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

            QWidget#panelIzquierdo {{
                background-color: {Styles.WHITE};
                color: {Styles.PRIMARY_TEXT};
                border-right: 1px solid {Styles.BORDER};
            }}

            QListWidget#menuLateral {{
                background-color: white;
                color: {Styles.PRIMARY_TEXT};
                border: none;
                font-weight: bold;
            }}

            QListWidget#menuLateral::item {{
                padding: 6px 12px;
            }}

            QListWidget#menuLateral::item:selected {{
                background-color: #d0e1ff;
                color: #1a2b4c;
            }}

            QWidget#contenedorTabla {{
                background-color: white;
            }}

            QComboBox QAbstractItemView {{
                background-color: white;
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                selection-background-color: {Styles.HIGHLIGHT};
                selection-color: {Styles.PRIMARY_TEXT};
            }}

            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                width: 20px;
                height: 12px;
                background-color: {Styles.WHITE};
                border-left: 1px solid {Styles.BORDER};
            }}

            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-bottom: 3px solid {Styles.PRIMARY_TEXT};
            }}

            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                border-left: 2px solid transparent;
                border-right: 2px solid transparent;
                border-top: 3px solid {Styles.PRIMARY_TEXT};
            }}

            QWidget#panelContenido {{
                background-color: transparent;
                border: none;
            }}

            QFrame#tarjeta {{
                background-color: white;
                border-radius: 20px;
                padding: 25px;
                min-width: 300px;
                border: 1px solid #e0e0e0;
            }}

            QFrame#tarjeta QLabel {{
                color: {Styles.PRIMARY_TEXT};
                background-color: white;
                font-size: 16px;
                font-weight: bold;
            }}

            QLabel#titulo {{
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 30px;
            }}

            QFrame#tarjeta QLabel#subtitulo {{
                font-size: 18px;
                margin-bottom: 10px;
            }}

            QFrame#tarjeta QLabel#dato {{
                font-size: 20px;
                margin: 5px 0 15px 0;
            }}

            QFrame#tarjeta QLabel#dato_inventario {{
                font-size: 16px;
                margin: 4px 0;
            }}

            QLabel#logoLabel {{
                margin-top: 20px;
                margin-bottom: 20px;
            }}

            QPushButton#menuButton {{
                border: none;
                background-color: white;
                font-size: 15px;
                color: #3f4c53;
                font-weight: bold;
                padding: 15px 0px;
            }}

            QPushButton#menuButton:hover {{
                background-color: #f0f0f0;
            }}

            QPushButton#menuButton:pressed {{
                background-color: #d0d0d0;
            }}
        """

