from Modelo.modeloPedido import Modelo
from Vista.verPedidos import VerPedidos

class VerPedidosControlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VerPedidos()
        self.pedidos = []
        self.pedido_actual = None
        
        # Conectar señales de la vista
        self.vista.pedido_seleccionado.connect(self.on_pedido_seleccionado)
        self.vista.eliminar_pedido_solicitado.connect(self.on_eliminar_pedido)
        
        self.cargar_pedidos()
    
    def cargar_pedidos(self):
        """Carga los pedidos desde el modelo y actualiza la vista"""
        try:
            self.pedidos = self.modelo.obtener_datos_pedido()
            self.vista.mostrar_lista_pedidos(self.pedidos)
        except Exception as e:
            self.vista.mostrar_mensaje_error(f"Error al cargar pedidos: {str(e)}")
    
    def on_pedido_seleccionado(self, indice):
        """Maneja la selección de un pedido"""
        if indice < 0 or indice >= len(self.pedidos):
            self.vista.limpiar_detalle()
            self.pedido_actual = None
            return
        
        self.pedido_actual = self.pedidos[indice]
        self.vista.mostrar_detalle_pedido(self.pedido_actual)
    
    def on_eliminar_pedido(self):
        """Maneja la eliminación de un pedido"""
        if not self.pedido_actual:
            self.vista.mostrar_mensaje_error("No hay pedido seleccionado")
            return
        
        numero_pedido = self.pedido_actual["numero"]
        
        # Confirmar eliminación
        if not self.vista.mostrar_confirmacion_eliminacion(numero_pedido):
            return
        
        try:
            # Eliminar en el modelo
            self.modelo.eliminar_pedido(numero_pedido)
            
            # Actualizar la lista local
            self.pedidos = [p for p in self.pedidos if p["numero"] != numero_pedido]
            
            # Actualizar la vista
            self.vista.mostrar_lista_pedidos(self.pedidos)
            self.vista.mostrar_mensaje_exito("Pedido eliminado correctamente.")
            
        except Exception as e:
            self.vista.mostrar_mensaje_error(f"Error al eliminar pedido: {str(e)}")
    
    def refrescar_datos(self):
        """Recarga los pedidos desde la base de datos"""
        self.cargar_pedidos()

    def get_vista(self):
        return self.vista    
    
