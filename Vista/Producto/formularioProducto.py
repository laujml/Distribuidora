# Vista/FormularioProductoView.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QSizePolicy
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
        self.setWindowTitle(titulo)
        self.setMinimumSize(500, 600)  # Tamaño mínimo más compacto
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz del formulario"""
        # Layout principal centrado
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)
        
        # Título
        titulo = QLabel(self.titulo_texto)
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(titulo)
        
        # Widget del formulario
        self.form_widget = QWidget()
        self.form_widget.setObjectName("form_widget")
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(8)  
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Crear campos del formulario
        self.crear_campos_formulario()
        
        # Crear botones
        self.crear_botones()
        
        # Agregar el form widget al layout principal
        main_layout.addWidget(self.form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def crear_campos_formulario(self):
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
        
        for i, (label_text, campo_db) in enumerate(campos):
            # Label del campo
            label = QLabel(label_text)
            label.setObjectName("campo_label")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.form_layout.addWidget(label)
            
            # Input del campo
            edit = QLineEdit()
            edit.setObjectName("campo_input")
            edit.setPlaceholderText(label_text)
            edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.form_layout.addWidget(edit)
            self.inputs[campo_db] = edit
            
            # Espaciado después del último campo
            if i == len(campos) - 1:
                self.form_layout.addSpacing(16)
    
    def crear_botones(self):
        """Crea los botones del formulario"""
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        
        # Botón de acción principal
        btn_accion = QPushButton(self.boton_texto)
        btn_accion.setObjectName("btn_primary")
        btn_accion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_accion.clicked.connect(self.ejecutar_accion)
        botones_layout.addWidget(btn_accion)
        
        # Botón buscar (si es necesario)
        if self.mostrar_buscar and self.accion != "buscar":
            btn_buscar = QPushButton("Buscar")
            btn_buscar.setObjectName("btn_primary")
            btn_buscar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn_buscar.clicked.connect(self.buscar_producto)
            botones_layout.addWidget(btn_buscar)
        
        # Botón para limpiar campos
        btn_otro = QPushButton(f"{self.boton_texto} otro producto")
        btn_otro.setObjectName("btn_primary")
        btn_otro.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_otro.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(btn_otro)

        # Botón regresar
        btn_regresar = QPushButton("← Regresar")
        btn_regresar.setObjectName("btn_secondary")
        btn_regresar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_regresar.clicked.connect(self.volver_inicio)
        botones_layout.addWidget(btn_regresar)

        self.form_layout.addLayout(botones_layout)

    
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
                self.inputs[campo].setText(str(valor) if valor else "")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        for input_widget in self.inputs.values():
            input_widget.clear()
    
    def volver_inicio(self):
        """Vuelve al menú principal - Delega al controlador"""
        self.limpiar_campos()
        self.controlador.volver_menu_principal()
    
    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra un mensaje al usuario"""
        mbox = QMessageBox(self)
        mbox.setWindowTitle(titulo)
        mbox.setText(mensaje)
        
        if tipo == "info":
            mbox.setIcon(QMessageBox.Icon.Information)
        elif tipo == "warning":
            mbox.setIcon(QMessageBox.Icon.Warning)
        elif tipo == "error":
            mbox.setIcon(QMessageBox.Icon.Critical)
        
        mbox.exec()
    
    def ejecutar_accion(self):
        self.controlador.vista_formulario = self  
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
