class Styles:
    """Clase para gestionar estilos de la interfaz de usuario de la aplicación de distribuidora."""
    
    # Paleta de colores más sobria
    BACKGROUND = "#4d5a62"  # Fondo más claro y sobrio
    BUTTON_BG = "#969a9a"   # Gris claro para botones
    BUTTON_HOVER = "#676d71"  # Gris más oscuro para hover
    BORDER = "#676d71"      # Color de bordes
    TEXT = "#969fa3"        # Color de texto
    LABEL_TEXT = "#969a9a"  # Color de texto para etiquetas

    @staticmethod
    def get_app_stylesheet():
        """Devuelve la hoja de estilos para toda la aplicación."""
        return f"""
            QWidget {{
                background-color: {Styles.BACKGROUND};
                color: {Styles.TEXT};
                font-family: Arial, sans-serif;
                font-size: 14px;
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
                padding: 8px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {Styles.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Styles.BACKGROUND};
            }}
        """

    @staticmethod
    def get_combo_box_stylesheet():
        """Devuelve la hoja de estilos para widgets QComboBox."""
        return f"""
            QComboBox {{
                background-color: {Styles.BACKGROUND};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 5px;
            }}
            QComboBox:hover {{
                background-color: {Styles.BUTTON_HOVER};
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
                background-color: {Styles.BACKGROUND};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 5px;
            }}
            QDateEdit:hover {{
                background-color: {Styles.BUTTON_HOVER};
            }}
            QDateEdit::drop-down {{
                border: none;
            }}
            QDateEdit::down-button, QDateEdit::up-button {{
                background-color: {Styles.BUTTON_BG};
            }}
        """

    @staticmethod
    def get_table_widget_stylesheet():
        """Devuelve la hoja de estilos para widgets QTableWidget."""
        return f"""
            QTableWidget {{
                background-color: {Styles.BACKGROUND};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                gridline-color: {Styles.BORDER};
            }}
            QTableWidget::item {{
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {Styles.BUTTON_HOVER};
            }}
            QHeaderView::section {{
                background-color: {Styles.BUTTON_BG};
                color: {Styles.TEXT};
                border: 1px solid {Styles.BORDER};
                padding: 4px;
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
        from PyQt6.QtWidgets import QPushButton, QComboBox, QDateEdit, QTableWidget, QLabel
        if isinstance(widget, QPushButton):
            widget.setStyleSheet(Styles.get_button_stylesheet())
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(Styles.get_combo_box_stylesheet())
        elif isinstance(widget, QDateEdit):
            widget.setStyleSheet(Styles.get_date_edit_stylesheet())
        elif isinstance(widget, QTableWidget):
            widget.setStyleSheet(Styles.get_table_widget_stylesheet())
        elif isinstance(widget, QLabel):
            widget.setStyleSheet(Styles.get_label_stylesheet())
        else:
            widget.setStyleSheet(Styles.get_app_stylesheet())
