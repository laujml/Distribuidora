from PyQt6.QtWidgets import QMessageBox
from Modelo.modeloPedido import Modelo
from Vista.Pedido.editarPedido import EditarPedido
from Controlador.Pedido.controladorCrearPedido import ControladorCrearPedidos

class ControladorEditarPedidos(ControladorCrearPedidos):
    def __init__(self):
        super().__init__()
        self.modelo = Modelo()
        self.vista = EditarPedido()
        self.pedidos = []
        self.pedido_actual = None
        
        # Conectar señales con métodos del controlador
        self.vista.pedido_seleccionado.connect(self.cargar_pedido_en_formulario)
        self.vista.guardar_cambios.connect(self.guardar_pedido)

        self.vista.agregar_producto_signal.connect(self.agregar_producto)
        self.vista.eliminar_fila_signal.connect(self.eliminar_fila)
        self.vista.cambiar_cantidad_signal.connect(self.cambiar_cantidad_fila)
        self.vista.resetear_pedido_signal.connect(self.resetear_pedido)

        self.cargar_productos()
        self.cargar_estados()
        self.cargar_clientes()
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        """Carga los datos iniciales del modelo"""
        try:
            self.pedidos = self.modelo.obtener_datos_pedido()
            self.vista.cargar_lista_pedidos(self.pedidos)
        except Exception as e:
            QMessageBox.critical(self.vista, "Error", f"Error al cargar pedidos: {e}")

    def cargar_pedido_en_formulario(self, index):
        """Carga un pedido específico en el formulario"""
        if index < 0 or index >= len(self.pedidos):
            return

        try:
            pedido = self.pedidos[index]
            self.pedido_actual = pedido
            self.vista.cargar_pedido_en_formulario(pedido)
            self.productos_seleccionados = self.vista.get_productos_seleccionados()
        except Exception as e:
            QMessageBox.critical(self.vista, "Error", f"Error al cargar pedido: {e}")

    def guardar_pedido(self):
        """Guarda los cambios del pedido actual"""
        if not self.pedido_actual:
            QMessageBox.warning(self.vista, "Advertencia", "No hay pedido seleccionado para guardar.")
            return

        try:
            datos_formulario = self.vista.obtener_datos_formulario()

            # Verificar si hay cliente
            if not datos_formulario['texto_cliente'].strip():
                QMessageBox.warning(self.vista, "Advertencia", "Debe seleccionar un cliente para guardar el pedido.")
                return

            # Verificar si hay productos
            if not datos_formulario['detalles']:
                QMessageBox.warning(self.vista, "Advertencia", "Debe agregar al menos un producto al pedido.")
                return

            # Extraer ID del cliente del texto
            id_cliente = datos_formulario['texto_cliente'].split("-")[0].strip() if "-" in datos_formulario['texto_cliente'] else datos_formulario['texto_cliente']
            
            # verificación de que el cliente existe
            clientes_validos = self.modelo.obtener_clientes()
            clientes_ids = [c.split("-")[0].strip() for c in clientes_validos]
            if id_cliente not in clientes_ids:
                QMessageBox.critical(self.vista, "Cliente no válido",
                                    "El cliente ingresado no existe. Selecciónelo desde el autocompletado.")
                return
            
            id_pedido = self.pedido_actual["numero"]

            # Actualizar pedido en el modelo
            exito = self.modelo.actualizar_pedido(
                id_pedido, 
                id_cliente, 
                datos_formulario['total'], 
                datos_formulario['estado'], 
                datos_formulario['pendiente'], 
                datos_formulario['plazo'], 
                datos_formulario['detalles']
            )

            if exito:
                QMessageBox.information(self.vista, "Éxito", f"Pedido #{id_pedido} actualizado correctamente.")
                # Recargar datos
                self.pedidos = self.modelo.obtener_datos_pedido()
                self.vista.actualizar_lista_pedidos(self.pedidos)
            else:
                QMessageBox.critical(self.vista, "Error", "Ocurrió un error al actualizar el pedido.")

        except Exception as e:
            QMessageBox.critical(self.vista, "Error", f"Error al guardar cambios: {e}")


    def refrescar_datos(self):
        """Refresca los datos desde el modelo"""
        
        self.cargar_datos_iniciales()

    def obtener_pedidos(self):
        """Getter para obtener la lista de pedidos"""
        return self.pedidos

    def obtener_pedido_actual(self):
        """Getter para obtener el pedido actual"""
        return self.pedido_actual
