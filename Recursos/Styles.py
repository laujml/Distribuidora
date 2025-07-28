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
            
            /* ===== ESTILOS PARA FORMULARIOS DE CLIENTES ===== */
            
            /* Labels de campos en formularios */
            QLabel#campo_label {{
                color: #fff;
                font-size: 12px;
                font-weight: 500;
                margin-bottom: 2px;
                font-family: 'Poppins', sans-serif;
            }}
            
            /* Inputs de texto en formularios */
            QLineEdit#campo_input {{
                background: #fff;
                border-radius: 15px;
                border: none;
                padding: 4px 12px;
                font-size: 12px;
                font-family: 'Poppins', sans-serif;
                min-height: 28px;
                max-height: 28px;
                color: #222;
            }}
            
            QLineEdit#campo_input:focus {{
                background: #f8f9fa;
                border: 2px solid #3498db;
            }}
            
            /* Botones de formularios - estilo común */
            QPushButton#btn_primary, QPushButton#btn_secondary {{
                background: #fff;
                color: {Styles.PRIMARY_TEXT};
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
                min-height: 28px;
                border: none;
            }}
            
            QPushButton#btn_primary:hover, QPushButton#btn_secondary:hover {{
                background-color: #eaeaea;
            }}
            
            QPushButton#btn_primary:pressed, QPushButton#btn_secondary:pressed {{
                background-color: #dcdcdc;
            }}
            
            /* Widget del formulario */
            QWidget#form_widget {{
                background: transparent;
            }}
            
            /* Botón del dashboard */
            QPushButton#btn_dashboard {{
                background: #fff;
                color: {Styles.PRIMARY_TEXT};
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
                min-height: 32px;
                border: 1px solid {Styles.PRIMARY_TEXT};
            }}
            
            QPushButton#btn_dashboard:hover {{
                background-color: #f0f0f0;
            }}
            
            QPushButton#btn_dashboard:pressed {{
                background-color: #e0e0e0;
            }}
            
            /* Botón de bienvenida */
            QPushButton#btn_bienvenida {{
                background: #fff;
                color: {Styles.PRIMARY_TEXT};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
                border: 1px solid {Styles.PRIMARY_TEXT};
            }}
            
            QPushButton#btn_bienvenida:hover {{
                background-color: #f0f0f0;
            }}
            
            QPushButton#btn_bienvenida:pressed {{
                background-color: #e0e0e0;
            }}
            
            /* Logo fallback (cuando no existe la imagen) */
            QLabel#logoLabel_fallback {{
                border: 2px solid white;
                border-radius: 120px;
                width: 240px;
                height: 240px;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            
            /* ===== ESTILOS PARA PANTALLA DE LOGIN ===== */
            
            /* Contenedor del login */
            QFrame#login_container {{
                background: transparent;
                border: none;
            }}
            
            /* Logo del login */
            QLabel#logo_login {{
                background: transparent;
            }}
            
            /* Logo fallback del login (cuando no existe la imagen) */
            QLabel#logo_login_fallback {{
                border: 2px solid white;
                border-radius: 50px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }}
            
            /* Inputs del login */
            QLineEdit#login_input {{
                background: #fff;
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                font-family: 'Poppins', sans-serif;
            }}
            
            QLineEdit#login_input:focus {{
                border: 2px solid #3498db;
                background: #f8f9fa;
            }}
            
            /* Botón primario del login */
            QPushButton#btn_login_primary {{
                background: #fff;
                color: {Styles.PRIMARY_TEXT};
                border: 1px solid {Styles.PRIMARY_TEXT};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
            }}
            
            QPushButton#btn_login_primary:hover {{
                background-color: #f0f0f0;
            }}
            
            QPushButton#btn_login_primary:pressed {{
                background-color: #e0e0e0;
            }}
            
            /* Botón secundario del login */
            QPushButton#btn_login_secondary {{
                background: transparent;
                color: white;
                border: 1px solid white;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Poppins', sans-serif;
            }}
            
            QPushButton#btn_login_secondary:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            
            QPushButton#btn_login_secondary:pressed {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
            
            /* ===== ESTILOS PARA REPORTES ===== */
            
            /* Etiquetas del resumen de estadísticas en reportes */
            QLabel#resumen_ventas {{
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: 2px solid #34495e;
                border-radius: 8px;
                margin: 5px;
                min-height: 20px;
                font-family: 'Poppins', sans-serif;
            }}
            
            QLabel#resumen_pedidos {{
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                margin: 5px;
                min-height: 20px;
                font-family: 'Poppins', sans-serif;
            }}
            
            QLabel#resumen_producto_top {{
                background-color: #e67e22;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: 2px solid #f39c12;
                border-radius: 8px;
                margin: 5px;
                min-height: 20px;
                font-family: 'Poppins', sans-serif;
            }}
            
            QLabel#resumen_cliente_top {{
                background-color: #8e44ad;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin: 5px;
                min-height: 20px;
                font-family: 'Poppins', sans-serif;
            }}
            
            /* Separador para reportes */
            QLabel#separador_reportes {{
                background-color: #bdc3c7;
                border: none;
                margin: 10px 0;
            }}
        """
