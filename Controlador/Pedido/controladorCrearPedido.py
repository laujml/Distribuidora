from PyQt6.QtWidgets import QMessageBox, QInputDialog
from Modelo.modeloPedido import Modelo
from Vista.Pedido.crearPedido import CrearPedidos

class ControladorCrearPedidos:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = CrearPedidos()
        self.total = 0.0
        self.productos_disponibles = {}
        self.productos_seleccionados = []

        # Conectar señales
        self.vista.agregar_producto_signal.connect(self.agregar_producto)
        self.vista.eliminar_fila_signal.connect(self.eliminar_fila)
        self.vista.cambiar_cantidad_signal.connect(self.cambiar_cantidad_fila)
        self.vista.guardar_pedido_signal.connect(self.guardar_pedido)
        self.vista.resetear_pedido_signal.connect(self.resetear_pedido)

        # Inicializar datos
        self.cargar_productos()
        self.cargar_clientes()
        self.cargar_estados()

    def cargar_productos(self):
        productos = self.modelo.obtener_productos()
        self.productos_disponibles.clear()
        lista_autocompletar = []

        for id_producto, descripcion, precio in productos:
            texto = f"{id_producto} - {descripcion}"
            lista_autocompletar.append(texto)
            self.productos_disponibles[texto] = (id_producto, descripcion, precio)

        self.vista.autocompletado_productos(lista_autocompletar)

    def cargar_clientes(self):
        clientes = self.modelo.obtener_clientes()
        self.vista.autocompletado_clientes(clientes)

    def cargar_estados(self):
        estados = self.modelo.obtener_estado()  # [(1, 'Pendiente'), (2, 'Pagado'), ...]
        self.vista.cargar_estados(estados)
    
    def agregar_producto(self, texto_producto, cantidad):
        if not texto_producto:
            QMessageBox.warning(self.vista, "Advertencia",
                                "Debe seleccionar un producto del autocompletado.")
            return

        if texto_producto not in self.productos_disponibles:
            QMessageBox.warning(self.vista, "Advertencia",
                                "Seleccione un producto válido del autocompletado.")
            return

        if cantidad <= 0:
            QMessageBox.warning(self.vista, "Cantidad inválida",
                                "La cantidad debe ser mayor que cero.")
            return

        id_producto, descripcion, precio = self.productos_disponibles[texto_producto]
        stock_disponible = self.modelo.obtener_stock_producto(id_producto)

        if stock_disponible == 0:
            QMessageBox.warning(self.vista, "Sin stock",
                                f"El producto '{descripcion}' no tiene stock disponible.")
            return

        if cantidad > stock_disponible:
            QMessageBox.warning(self.vista, "Stock insuficiente",
                                f"Solo hay {stock_disponible} unidades disponibles de '{descripcion}'.")
            return

        subtotal = float(precio * cantidad)

        # Actualizar vista y controlador
        self.vista.agregar_fila_tabla(id_producto, descripcion, precio, cantidad, subtotal)
        self.productos_seleccionados.append([id_producto, cantidad, subtotal])
        self.actualizar_total()

    def actualizar_total(self):
        self.total = sum(float(item[2]) for item in self.productos_seleccionados)
        self.vista.actualizar_total(self.total)

    def eliminar_fila(self, fila):
        if fila == -1:
            QMessageBox.warning(self.vista, "Advertencia",
                                "Seleccione una fila para eliminar.")
            return

        respuesta = QMessageBox.question(
            self.vista, "Confirmar eliminación",
            "¿Está seguro de eliminar la fila seleccionada?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.vista.eliminar_fila_tabla(fila)
            self.productos_seleccionados.pop(fila)
            self.actualizar_total()

    def cambiar_cantidad_fila(self, fila, cantidad_actual):
        if fila == -1:
            QMessageBox.warning(self.vista, "Advertencia",
                                "Seleccione una fila para cambiar la cantidad.")
            return

        nuevo_valor, ok = QInputDialog.getInt(
            self.vista, "Cambiar cantidad",
            "Ingrese nueva cantidad:",
            value=cantidad_actual, min=1
        )

        if ok:
            descripcion = self.vista.obtener_descripcion_fila(fila)

            # Buscar producto y validar stock
            for key, (id_prod, desc, precio) in self.productos_disponibles.items():
                if desc == descripcion:
                    stock_disponible = self.modelo.obtener_stock_producto(id_prod)

                    if nuevo_valor > stock_disponible:
                        QMessageBox.warning(self.vista, "Stock insuficiente",
                                            f"Solo hay {stock_disponible} unidades disponibles.")
                        return

                    nuevo_subtotal = precio * nuevo_valor

                    self.vista.actualizar_cantidad_fila(fila, nuevo_valor, nuevo_subtotal)
                    self.productos_seleccionados[fila][1] = nuevo_valor
                    self.productos_seleccionados[fila][2] = nuevo_subtotal
                    break

            self.actualizar_total()

    def guardar_pedido(self, texto_cliente, estado, pendiente_pagar, plazo_dias):
        try:
            if not texto_cliente.strip():
                QMessageBox.warning(self.vista, "Advertencia",
                                    "Debe seleccionar un cliente.")
                return

            if not self.productos_seleccionados:
                QMessageBox.warning(self.vista, "Advertencia",
                                    "No hay productos en el pedido.")
                return

            id_cliente = texto_cliente.split("-")[0].strip() if "-" in texto_cliente else texto_cliente

            id_pedido = self.modelo.crear_pedido(
                id_cliente, self.total, estado, pendiente_pagar, plazo_dias
            )

            self.modelo.agregar_detalle_y_actualizar_stock(id_pedido, self.productos_seleccionados)

            QMessageBox.information(self.vista, "Éxito",
                                    f"Pedido #{id_pedido} guardado correctamente.")
            self.resetear_pedido()

        except Exception as e:
            QMessageBox.critical(self.vista, "Error",
                                 f"No se pudo guardar el pedido:\n{e}")

    def resetear_pedido(self):
        self.vista.limpiar()
        self.total = 0.0
        self.productos_seleccionados.clear()

    def mostrar_vista(self):
        self.vista.show()

    def get_vista(self):
        return self.vista

