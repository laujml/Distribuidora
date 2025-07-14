class Styles:
    """Estilos generales reutilizables para la aplicación."""

    PRIMARY_TEXT = "#4d5a62"  # Azul sobrio
    BACKGROUND = "#4d5a62"    # Fondo gris oscuro general
    WHITE = "#ffffff"
    BORDER = "#dee2e6"
    HIGHLIGHT = "#f5f7fa"

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

            /* Estilo para el número de pedido */
            QLabel#pedidoNumero {{
                background-color: {Styles.WHITE};
                color: {Styles.PRIMARY_TEXT};
                font-size: 14px;
                font-weight: bold;
                padding: 6px 8px;
                border-radius: 4px;
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

            QSpinBox::up-button, QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 16px;
            border-left: 1px solid {Styles.BORDER};
            border-bottom: 1px solid {Styles.BORDER};
            background-color: {Styles.WHITE};
            }}

            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid {Styles.BORDER};
                border-top: 1px solid {Styles.BORDER};
                background-color: {Styles.WHITE};
            }}

            /* Cambiar color de fondo de botones al hacer hover */
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
                background-color: #e6f0ff;
            }}

            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
                background-color: #e6f0ff;
            }}
        """
    
