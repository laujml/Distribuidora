from model import ProveedorModel
from views import BaseProveedorVentana, VentanaPrincipalProveedor

class ProveedorController:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget

        self.model = ProveedorModel(parent_widget=None)  # Lo actualizaremos en cada vista
        self.ventana_inicio = VentanaPrincipalProveedor(stacked_widget)
        self.ventana_agregar = BaseProveedorVentana(stacked_widget, "Agregar Proveedor", "guardar", "Guardar")
        self.ventana_eliminar = BaseProveedorVentana(stacked_widget, "Eliminar Proveedor", "eliminar", "Eliminar")
        self.ventana_actualizar = BaseProveedorVentana(stacked_widget, "Actualizar Proveedor", "actualizar", "Actualizar")
        self.ventana_buscar = BaseProveedorVentana(stacked_widget, "Buscar Proveedor", "buscar", "Buscar")

        stacked_widget.addWidget(self.ventana_inicio)
        stacked_widget.addWidget(self.ventana_agregar)
        stacked_widget.addWidget(self.ventana_eliminar)
        stacked_widget.addWidget(self.ventana_actualizar)
        stacked_widget.addWidget(self.ventana_buscar)

        self.conectar_signales()

    def conectar_signales(self):
        # Guardar
        self.ventana_agregar.btn_accion.clicked.connect(self.guardar_proveedor)
        self.ventana_agregar.btn_regresar.clicked.connect(self.regresar_inicio)
        self.ventana_agregar.btn_otro.clicked.connect(self.ventana_agregar.limpiar_campos)

        # Eliminar
        self.ventana_eliminar.btn_accion.clicked.connect(self.eliminar_proveedor)
        self.ventana_eliminar.btn_regresar.clicked.connect(self.regresar_inicio)
        self.ventana_eliminar.btn_buscar.clicked.connect(self.consultar_proveedor)
        self.ventana_eliminar.btn_otro.clicked.connect(self.ventana_eliminar.limpiar_campos)

        # Actualizar
        self.ventana_actualizar.btn_accion.clicked.connect(self.actualizar_proveedor)
        self.ventana_actualizar.btn_regresar.clicked.connect(self.regresar_inicio)
        self.ventana_actualizar.btn_buscar.clicked.connect(self.consultar_proveedor)
        self.ventana_actualizar.btn_otro.clicked.connect(self.ventana_actualizar.limpiar_campos)

        # Buscar (solo buscar)
        self.ventana_buscar.btn_regresar.clicked.connect(self.regresar_inicio)

    def regresar_inicio(self):
        self.ventana_agregar.limpiar_campos()
        self.ventana_eliminar.limpiar_campos()
        self.ventana_actualizar.limpiar_campos()
        self.ventana_buscar.limpiar_campos()
        self.stacked_widget.setCurrentIndex(0)

    def guardar_proveedor(self):
        datos = tuple(self.ventana_agregar.inputs[c].text() for c in self.ventana_agregar.inputs)
        self.model.parent_widget = self.ventana_agregar
        self.model.guardar_proveedor(datos)

    def eliminar_proveedor(self):
        id_proveedor = self.ventana_eliminar.inputs["id_proveedor"].text()
        self.model.parent_widget = self.ventana_eliminar
        self.model.eliminar_proveedor(id_proveedor)
        self.ventana_eliminar.limpiar_campos()

    def actualizar_proveedor(self):
        datos = (
            self.ventana_actualizar.inputs["proveedor"].text(),
            self.ventana_actualizar.inputs["p_contacto"].text(),
            self.ventana_actualizar.inputs["correo"].text(),
            self.ventana_actualizar.inputs["telefono"].text(),
            self.ventana_actualizar.inputs["direccion_proveedor"].text(),
            self.ventana_actualizar.inputs["id_proveedor"].text(),
        )
        self.model.parent_widget = self.ventana_actualizar
        self.model.actualizar_proveedor(datos)

    def consultar_proveedor(self):
        # Se usa tanto en eliminar como en actualizar
        if self.stacked_widget.currentIndex() == 2:
            ventana = self.ventana_eliminar
        else:
            ventana = self.ventana_actualizar

        id_proveedor = ventana.inputs["id_proveedor"].text()
        self.model.parent_widget = ventana
        resultado = self.model.consultar_proveedor(id_proveedor)
        if resultado:
            keys = ["proveedor", "p_contacto", "correo", "telefono", "direccion_proveedor"]
            for k, v in zip(keys, resultado):
                ventana.inputs[k].setText(v)
            QMessageBox.information(ventana, "Consulta exitosa", "Proveedor encontrado.")
        else:
            QMessageBox.warning(ventana, "No encontrado", "Proveedor no registrado.")
