from PyQt6.QtWidgets import QMessageBox, QFileDialog
import pandas as pd
from Modelo.modelo_productos import ProductoModel

class ProductoController:
    def __init__(self):
        self.modelo = ProductoModel()
        self.vista_menu = None
        self.vista_tabla = None
        self.vista_formulario = None
        self.vistas_formulario = {}

    def guardar_producto(self):
        try:
            datos_formulario = self.vista_formulario.obtener_datos_formulario()
            if not all(datos_formulario.values()):
                self.vista_formulario.mostrar_mensaje("warning", "Campos vacíos", "Completa todos los campos.")
                return
            datos_producto = (
                datos_formulario["id_productos"],
                datos_formulario["descripcion"],
                datos_formulario["precio"],
                datos_formulario["talla"],
                datos_formulario["color"],
                datos_formulario["stockActual"],
                datos_formulario["fecha_ingreso"],
                datos_formulario["id_proveedor"]
            )
            filas_afectadas = self.modelo.insertar_producto(datos_producto)
            if filas_afectadas > 0:
                self.vista_formulario.mostrar_mensaje("info", "Éxito", "Producto guardado correctamente.")
                self.vista_formulario.limpiar_campos()
            else:
                self.vista_formulario.mostrar_mensaje("error", "Error", "No se pudo guardar el producto.")
        except Exception as e:
            self.vista_formulario.mostrar_mensaje("error", "Error", f"No se pudo guardar: {e}")

    def eliminar_producto(self):
        try:
            id_producto = self.vista_formulario.obtener_id_producto()
            if not id_producto:
                self.vista_formulario.mostrar_mensaje("warning", "Campo vacío", "Ingresa el ID del producto.")
                return
            filas_afectadas = self.modelo.eliminar_producto(id_producto)
            if filas_afectadas > 0:
                self.vista_formulario.mostrar_mensaje("info", "Eliminado", "Producto eliminado.")
                self.vista_formulario.limpiar_campos()
            else:
                self.vista_formulario.mostrar_mensaje("warning", "No encontrado", "Producto no existe.")
        except Exception as e:
            self.vista_formulario.mostrar_mensaje("error", "Error", f"Error al eliminar: {e}")

    def actualizar_producto(self):
        try:
            datos_formulario = self.vista_formulario.obtener_datos_formulario()
            if not all(datos_formulario.values()):
                self.vista_formulario.mostrar_mensaje("warning", "Campos vacíos", "Completa todos los campos.")
                return
            datos_producto = (
                datos_formulario["descripcion"],
                datos_formulario["precio"],
                datos_formulario["talla"],
                datos_formulario["color"],
                datos_formulario["stockActual"],
                datos_formulario["fecha_ingreso"],
                datos_formulario["id_proveedor"],
                datos_formulario["id_productos"]
            )
            filas_afectadas = self.modelo.actualizar_producto(datos_producto)
            if filas_afectadas > 0:
                self.vista_formulario.mostrar_mensaje("info", "Actualizado", "Producto actualizado.")
            else:
                self.vista_formulario.mostrar_mensaje("warning", "No encontrado", "Producto no encontrado.")
        except Exception as e:
            self.vista_formulario.mostrar_mensaje("error", "Error", f"Error al actualizar: {e}")

    def buscar_producto(self):
        try:
            id_producto = self.vista_formulario.obtener_id_producto()
            if not id_producto:
                self.vista_formulario.mostrar_mensaje("warning", "Campo vacío", "Ingresa el ID del producto.")
                return
            resultado = self.modelo.buscar_producto_por_id(id_producto)
            if resultado:
                datos = {
                    "id_productos": str(resultado[0]) if resultado[0] is not None else "",
                    "descripcion": str(resultado[1]) if resultado[1] is not None else "",
                    "precio": str(resultado[2]) if resultado[2] is not None else "",
                    "talla": str(resultado[3]) if resultado[3] is not None else "",
                    "color": str(resultado[4]) if resultado[4] is not None else "",
                    "stockActual": str(resultado[5]) if resultado[5] is not None else "",
                    "fecha_ingreso": str(resultado[6]) if resultado[6] is not None else "",
                    "id_proveedor": str(resultado[7]) if resultado[7] is not None else ""
                }
                self.vista_formulario.llenar_formulario(datos)
                self.vista_formulario.mostrar_mensaje("info", "Encontrado", "Producto encontrado.")
            else:
                self.vista_formulario.mostrar_mensaje("warning", "No encontrado", "Producto no existe.")
        except Exception as e:
            self.vista_formulario.mostrar_mensaje("error", "Error", f"Error al buscar: {e}")

    def cargar_tabla_productos(self):
        try:
            productos = self.modelo.obtener_todos_productos()
            self.vista_tabla.actualizar_tabla(productos)
        except Exception as e:
            self.vista_tabla.mostrar_error(f"No se pudo cargar la tabla: {e}")

    def importar_desde_excel(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.vista_tabla,
                "Seleccionar archivo Excel",
                "",
                "Excel Files (*.xlsx *.xls)"
            )
            if not file_path:
                return
            df = pd.read_excel(file_path)
            columnas_requeridas = [
                "ID Producto", "Descripción", "Precio", "Talla",
                "Color", "Stock", "Fecha de Ingreso", "ID Proveedor"
            ]
            columnas_normalizadas = [col.lower().strip() for col in df.columns]
            requeridas_normalizadas = [c.lower() for c in columnas_requeridas]
            if not all(col in columnas_normalizadas for col in requeridas_normalizadas):
                mensaje = f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}"
                self.vista_tabla.mostrar_error(mensaje)
                return
            mapeo = {
                "ID Producto": "id_productos",
                "Descripción": "descripcion",
                "Precio": "precio",
                "Talla": "talla",
                "Color": "color",
                "Stock": "stockActual",
                "Fecha de Ingreso": "fecha_ingreso",
                "ID Proveedor": "id_proveedor"
            }
            df = df.rename(columns={col: mapeo[col] for col in columnas_requeridas})
            lista_productos = []
            for _, fila in df.iterrows():
                datos = (
                    str(fila["id_productos"]),
                    str(fila["descripcion"]),
                    float(fila["precio"]),
                    str(fila["talla"]),
                    str(fila["color"]),
                    int(fila["stockActual"]),
                    str(fila["fecha_ingreso"]),
                    str(fila["id_proveedor"])
                )
                lista_productos.append(datos)
            insertados, actualizados = self.modelo.insertar_productos_masivo(lista_productos)
            mensaje = f"Productos importados: {insertados} nuevos, {actualizados} actualizados."
            self.vista_tabla.mostrar_exito(mensaje)
            self.cargar_tabla_productos()
        except Exception as e:
            self.vista_tabla.mostrar_error(f"Error al importar: {e}")

    def navegar_a_vista(self, indice_vista):
        if self.vista_menu and hasattr(self.vista_menu, 'stacked_widget'):
            self.vista_menu.stacked_widget.setCurrentIndex(indice_vista)
            # Actualizar referencia de vista_formulario según índice
            self.vista_formulario = self.vistas_formulario.get(indice_vista, None)

    def volver_menu_principal(self):
        if self.vista_formulario:
            self.vista_formulario.limpiar_campos()
        self.navegar_a_vista(0)
