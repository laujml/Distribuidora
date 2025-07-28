from PyQt6.QtWidgets import QMessageBox, QFileDialog
import pandas as pd
from Modelo.modelo_productos import ProductoModel
from datetime import datetime

class ProductoController:
    def __init__(self):
        self.modelo = ProductoModel()
        self.vista_menu = None
        self.vista_tabla = None
        self.vista_formulario = None
        self.vistas_formulario = {}

    def validar_datos_producto(self, datos):
        errores = []

        # Validar precio
        try:
            datos["precio"] = float(datos["precio"])
        except ValueError:
            errores.append("El campo 'Precio' debe ser un número.")

        # Validar talla
        try:
            datos["talla"] = float(datos["talla"])
        except ValueError:
            errores.append("El campo 'Talla' debe ser un número.")

        # Validar stock
        try:
            datos["stockActual"] = int(datos["stockActual"])
        except ValueError:
            errores.append("El campo 'Stock' debe ser un número entero.")

        # Validar fecha
        try:
            datetime.strptime(datos["fecha_ingreso"], "%Y-%m-%d")
        except ValueError:
            errores.append("La 'Fecha de Ingreso' debe tener el formato YYYY-MM-DD.")

        # Validar proveedor existente
        if not self.modelo.proveedor_existe(datos["id_proveedor"]):
            errores.append(f"El proveedor con ID '{datos['id_proveedor']}' no existe.")

        return errores    

    def guardar_producto(self):
        try:
            datos_formulario = self.vista_formulario.obtener_datos_formulario()

            # Verificar campos vacíos
            if not all(datos_formulario.values()):
                self.vista_formulario.mostrar_mensaje("warning", "Campos vacíos", "Completa todos los campos.")
                return

            # Validar datos
            errores = self.validar_datos_producto(datos_formulario)
            if errores:
                mensaje_error = "\n".join(errores)
                self.vista_formulario.mostrar_mensaje("warning", "Errores de validación", mensaje_error)
                return

            # Preparar tupla con datos ya convertidos
            datos_producto = (
                datos_formulario["id_productos"],
                datos_formulario["descripcion"],
                float(datos_formulario["precio"]),
                float(datos_formulario["talla"]),
                datos_formulario["color"],
                int(datos_formulario["stockActual"]),
                datos_formulario["fecha_ingreso"],
                datos_formulario["id_proveedor"]
            )

            filas_afectadas = self.modelo.insertar_producto(datos_producto)

            if filas_afectadas > 0:
                self.vista_formulario.mostrar_mensaje("info", "Éxito", "Producto guardado correctamente.")
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

            # Validaciones
            errores = self.validar_datos_producto(datos_formulario)
            if errores:
                mensaje_error = "\n".join(errores)
                self.vista_formulario.mostrar_mensaje("warning", "Errores de validación", mensaje_error)
                return

            # Preparar tupla para la actualización (sin ID primero, que va al final)
            datos_producto = (
                datos_formulario["descripcion"],
                float(datos_formulario["precio"]),
                float(datos_formulario["talla"]),
                datos_formulario["color"],
                int(datos_formulario["stockActual"]),
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
            errores_excel = []

            for i, fila in df.iterrows():
                datos_dict = {
                    "id_productos": str(fila["id_productos"]),
                    "descripcion": str(fila["descripcion"]),
                    "precio": fila["precio"],
                    "talla": fila["talla"],
                    "color": str(fila["color"]),
                    "stockActual": fila["stockActual"],
                    "fecha_ingreso": str(fila["fecha_ingreso"]),
                    "id_proveedor": str(fila["id_proveedor"])
                }

                # Convertir a string todos los valores
                datos_dict = {k: str(v) for k, v in datos_dict.items()}

                errores = self.validar_datos_producto(datos_dict)

                if errores:
                    errores_excel.append(f"Fila {i+2}: " + "; ".join(errores))  # +2 por encabezado y 0-based index
                    continue  # saltar esta fila

                try:
                    datos = (
                        datos_dict["id_productos"],
                        datos_dict["descripcion"],
                        float(datos_dict["precio"]),
                        float(datos_dict["talla"]),
                        datos_dict["color"],
                        int(datos_dict["stockActual"]),
                        datos_dict["fecha_ingreso"],
                        datos_dict["id_proveedor"]
                    )
                    lista_productos.append(datos)
                except ValueError as e:
                    errores_excel.append(f"Fila {i+2}: Datos numéricos inválidos. Verifica que Precio, Talla y Stock sean números.")
                except Exception as e:
                    errores_excel.append(f"Fila {i+2}: Error inesperado al procesar la fila.")


            if lista_productos:
                insertados, actualizados = self.modelo.insertar_productos_masivo(lista_productos)
                mensaje = f"Productos importados: {insertados} nuevos, {actualizados} actualizados."
                self.vista_tabla.mostrar_exito(mensaje)
                self.cargar_tabla_productos()
            else:
                self.vista_tabla.mostrar_error("No se pudo importar ningún producto válido.")

            if errores_excel:
                mensaje_errores = "\n".join(errores_excel[:10])
                if len(errores_excel) > 10:
                    mensaje_errores += f"\n...y {len(errores_excel) - 10} errores más."
                self.vista_tabla.mostrar_error(f"Errores encontrados:\n{mensaje_errores}")

        except Exception as e:
            self.vista_tabla.mostrar_error(f"Error al importar: {e}")


    def navegar_a_vista(self, indice_vista):
        if self.vista_menu and hasattr(self.vista_menu, 'stacked_widget'):
            self.vista_menu.stacked_widget.setCurrentIndex(indice_vista)
            self.vista_formulario = self.vistas_formulario.get(indice_vista, None)

            if indice_vista == 3 and self.vista_tabla:
                self.cargar_tabla_productos()

    def volver_menu_principal(self):
        if self.vista_formulario:
            self.vista_formulario.limpiar_campos()
        self.navegar_a_vista(0)
