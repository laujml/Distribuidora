# Vista/FormularioProductoView.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt

class FormularioProductoView(QWidget):
    """Vista base para formularios de productos (agregar, actualizar, eliminar, buscar)"""
    
    def __init__(self, stacked_widget, titulo, accion, boton_texto, controlador, mostrar_buscar=True):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.accion = accion
        self.titulo_texto = titulo
        self.boton_texto = boton_texto
        self.mostrar_buscar = mostrar_buscar
        self.controlador = controlador  # Referencia al controlador
        self.inputs = {}
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz del formulario"""
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget principal
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)
        
        # Título
        titulo = QLabel(self.titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)
        
        # Crear campos del formulario
        self.crear_campos_formulario(layout)
        
        # Crear botones
        self.crear_botones(layout)
        
        # Botón regresar
        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_inicio)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Configurar scroll
        scroll_area.setWidget(content_widget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
    def crear_campos_formulario(self, layout):
        """Crea los campos del formulario"""
        campos = [
            ("ID Producto", "id_productos"),
            ("Descripción", "descripcion"),
            ("Precio", "precio"),
            ("Talla", "talla"),
            ("Color", "color"),
            ("Stock", "stockActual"),
            ("Fecha de Ingreso (YYYY-MM-DD)", "fecha_ingreso"),
            ("ID Proveedor", "id_proveedor")
        ]
        
        for label_text, campo_db in campos:
            label = QLabel(label_text)
            edit = QLineEdit()
            edit.setPlaceholderText(label_text)
            layout.addWidget(label)
            layout.addWidget(edit)
            self.inputs[campo_db] = edit
    
    def crear_botones(self, layout):
        """Crea los botones del formulario"""
        botones_layout = QHBoxLayout()
        
        # Botón de acción principal
        btn_accion = QPushButton(self.boton_texto)
        btn_accion.clicked.connect(self.ejecutar_accion)
        botones_layout.addWidget(btn_accion)
        
        # Botón buscar (si es necesario)
        if self.mostrar_buscar and self.accion != "buscar":
            btn_buscar = QPushButton("Buscar")
            btn_buscar.clicked.connect(self.buscar_producto)
            botones_layout.addWidget(btn_buscar)
        
        # Botón para limpiar campos
        btn_otro = QPushButton(f"{self.boton_texto} otro producto")
        btn_otro.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(btn_otro)
        
        layout.addLayout(botones_layout)
    
    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario como diccionario"""
        return {campo: input_widget.text() for campo, input_widget in self.inputs.items()}
    
    def obtener_id_producto(self):
        """Obtiene solo el ID del producto"""
        return self.inputs["id_productos"].text()
    
    def llenar_formulario(self, datos):
        """Llena el formulario con datos"""
        for campo, valor in datos.items():
            if campo in self.inputs:
                self.inputs[campo].setText(valor)
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for input_widget in self.inputs.values():
            input_widget.clear()
    
    def volver_inicio(self):
        """Vuelve al menú principal - Delega al controlador"""
        self.controlador.volver_menu_principal()
    
    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra un mensaje al usuario"""
        if tipo == "info":
            QMessageBox.information(self, titulo, mensaje)
        elif tipo == "warning":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "error":
            QMessageBox.critical(self, titulo, mensaje)
    
    def ejecutar_accion(self):
        self.controlador.vista_formulario = self  # <-- aseguramos que no sea None
        if self.accion == "guardar":
            self.controlador.guardar_producto()
        elif self.accion == "eliminar":
            self.controlador.eliminar_producto()
        elif self.accion == "actualizar":
            self.controlador.actualizar_producto()
        elif self.accion == "buscar":
            self.controlador.buscar_producto()

    def buscar_producto(self):
        """Busca un producto - Delega al controlador"""
        self.controlador.buscar_producto()
