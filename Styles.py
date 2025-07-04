class Styles:
    """Clase para gestionar estilos de la interfaz de usuario de la aplicación de distribuidora."""
    
    # Paleta de colores definida como variables de clase para fácil acceso y modificación
    BACKGROUND = "#1d222e"  # Fondo oscuro para la aplicación
    WIDGET_BG = "#4d5a62"   # Fondo para widgets como combo boxes y tablas
    BUTTON_BG = "#40464b"   # Fondo para botones
    BORDER = "#676d71"      # Color de bordes para widgets
    TEXT = "#969fa3"        # Color de texto para la mayoría de los widgets
    LABEL_TEXT = "#969a9a"  # Color de texto para etiquetas
    BUTTON_HOVER = "#676d71"  # Cambio de color al pasar el ratón sobre botones

    @staticmethod
    def get_app_stylesheet():
        """Devuelve la hoja de estilos para toda la aplicación."""
        return f"""
            QWidget {{
                background-color: {Styles.BACKGROUND};
                color: {Styles.TEXT};
            }}
        """

    @staticmethod
    def get_button_stylesheet():
        """Devuelve la hoja de estilos para widgets QPushButton."""
        return f"""
            QPushButton {{
                background-color: {Styles.BUTTON_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {Styles.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Styles.WIDGET_BG};
            }}
        """

    @staticmethod
    def get_combo_box_stylesheet():
        """Devuelve la hoja de estilos para widgets QComboBox."""
        return f"""
            QComboBox {{
                background-color: {Styles.WIDGET_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 3px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                width: 10px;
                height: 10px;
            }}
        """

    @staticmethod
    def get_date_edit_stylesheet():
        """Devuelve la hoja de estilos para widgets QDateEdit."""
        return f"""
            QDateEdit {{
                background-color: {Styles.WIDGET_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 3px;
            }}
            QDateEdit::drop-down {{
                border: none;
            }}
        """

    @staticmethod
    def get_table_view_stylesheet():
        """Devuelve la hoja de estilos para widgets QTableView."""
        return f"""
            QTableView {{
                background-color: {Styles.WIDGET_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                gridline-color: {Styles.BORDER};
            }}
            QTableView::item {{
                border: none;
            }}
            QHeaderView::section {{
                background-color: {Styles.BUTTON_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
            }}
        """

    @staticmethod
    def get_label_stylesheet():
        """Devuelve la hoja de estilos para widgets QLabel."""
        return f"""
            QLabel {{
                color: {Styles.LABEL_TEXT};
                background-color: transparent;
            }}
        """

    @staticmethod
    def apply_styles(widget):
        """Aplica la hoja de estilos adecuada según el tipo de widget."""
        from PyQt6.QtWidgets import QPushButton, QComboBox, QDateEdit, QTableView, QLabel
        if isinstance(widget, QPushButton):
            widget.setStyleSheet(Styles.get_button_stylesheet())
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(Styles.get_combo_box_stylesheet())
        elif isinstance(widget, QDateEdit):
            widget.setStyleSheet(Styles.get_date_edit_stylesheet())
        elif isinstance(widget, QTableView):
            widget.setStyleSheet(Styles.get_table_view_stylesheet())
        elif isinstance(widget, QLabel):
            widget.setStyleSheet(Styles.get_label_stylesheet())
        else:
            widget.setStyleSheet(Styles.get_app_stylesheet())