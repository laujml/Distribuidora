import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt
from Modelo.db_config import conectar

class BaseProductoVentana(QWidget):
    def __init__(self, stacked_widget, titulo, accion, boton_texto, mostrar_buscar=True):
        super().__init__()
        #Inicializacion de elementos
        self.stacked_widget = stacked_widget
        self.accion = accion
        self.titulo_texto = titulo
        self.boton_texto = boton_texto
        self.mostrar_buscar = mostrar_buscar
        self.ventanaProductos()

    def ventanaProductos(self):
        #Area de scroll para adecuarse la pantalla
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        #widget principal
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        #titulo
        titulo = QLabel(self.titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)

        self.inputs = {}

        #formulario
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

        #Recorrido de tupla para crear fomulario
        for label_text, campo_db in campos:
            label = QLabel(label_text)
            edit = QLineEdit()
            edit.setPlaceholderText(label_text)
            layout.addWidget(label)
            layout.addWidget(edit)
            self.inputs[campo_db] = edit

        botones_layout = QHBoxLayout()

        #boton de accion que luego sera instaciado segun el caso
        btn_accion = QPushButton(self.boton_texto)
        btn_accion.clicked.connect(self.ejecutar_accion)
        botones_layout.addWidget(btn_accion)

        #acciones del boton
        if self.mostrar_buscar and self.accion != "buscar":
            btn_buscar = QPushButton("Buscar")
            btn_buscar.clicked.connect(self.buscar_producto)
            botones_layout.addWidget(btn_buscar)

        btn_otro = QPushButton(f"{self.boton_texto} otro producto")
        btn_otro.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(btn_otro)

        layout.addLayout(botones_layout)

        #boton para regresar a la pantalla principal de productos
        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_inicio)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        #agregar el contenido al scroll
        scroll_area.setWidget(content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def conectar_db(self):
        return conectar()

    #limpiar formulario
    def limpiar_campos(self):
        for input in self.inputs.values():
            input.clear()

    def volver_inicio(self):
        self.limpiar_campos()
        self.stacked_widget.setCurrentIndex(0)
        
    #antes se definicio un boton para después instaciarlo dependiendo de lo que se necesite
    def ejecutar_accion(self):
        if self.accion == "guardar":
            self.guardar_producto()
        elif self.accion == "eliminar":
            self.eliminar_producto()
        elif self.accion == "actualizar":
            self.actualizar_producto()
        elif self.accion == "buscar":
            self.buscar_producto()

    def guardar_producto(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            #Consulta a la base para hacer insercciones de al guardar productos nuevos
            sql = """INSERT INTO productos 
            (ID_Productos, descripcion, precio, talla, color, stockActual, fecha_ingreso, ID_Proveedor) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            datos = (
                self.inputs["id_productos"].text(),
                self.inputs["descripcion"].text(),
                self.inputs["precio"].text(),
                self.inputs["talla"].text(),
                self.inputs["color"].text(),
                self.inputs["stockActual"].text(),
                self.inputs["fecha_ingreso"].text(),
                self.inputs["id_proveedor"].text()
            )
            if not all(datos):
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
                return
            cursor.execute(sql, datos)
            conn.commit()
            QMessageBox.information(self, "Éxito", "Producto guardado correctamente.")
            self.limpiar_campos()
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def eliminar_producto(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            #se selecciona el producto a eliminar por id
            id_producto = self.inputs["id_productos"].text()
            if not id_producto:
                QMessageBox.warning(self, "Campo vacío", "Ingresa el ID del producto.")
                return
                
            #consulta para eliminar
            sql = "DELETE FROM productos WHERE ID_Productos = %s"
            cursor.execute(sql, (id_producto,))
            conn.commit()
            if cursor.rowcount:
                QMessageBox.information(self, "Eliminado", "Producto eliminado.")
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "No encontrado", "Producto no existe.")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar: {e}")

    def actualizar_producto(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            #Consulta para actualizar un producto
            sql = """UPDATE productos SET descripcion=%s, precio=%s, talla=%s, color=%s, 
                     stockActual=%s, fecha_ingreso=%s, ID_Proveedor=%s 
                     WHERE ID_Productos=%s"""
            
            #datos del formulario
            datos = (
                self.inputs["descripcion"].text(),
                self.inputs["precio"].text(),
                self.inputs["talla"].text(),
                self.inputs["color"].text(),
                self.inputs["stockActual"].text(),
                self.inputs["fecha_ingreso"].text(),
                self.inputs["id_proveedor"].text(),
                self.inputs["id_productos"].text()
            )
            if not all(datos):
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
                return
            cursor.execute(sql, datos)
            conn.commit()
            if cursor.rowcount:
                QMessageBox.information(self, "Actualizado", "Producto actualizado.")
            else:
                QMessageBox.warning(self, "No encontrado", "Producto no encontrado.")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar: {e}")

    def buscar_producto(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            
            #buscar producto por id
            id_producto = self.inputs["id_productos"].text()
            if not id_producto:
                QMessageBox.warning(self, "Campo vacío", "Ingresa el ID del producto.")
                return
                
            #consulta para obtener los resultados de la busqueda    
            sql = "SELECT * FROM productos WHERE ID_Productos = %s"
            cursor.execute(sql, (id_producto,))
            resultado = cursor.fetchone()
            if resultado:
                #llenar los campos con los resultados de la busqueda
                campos = [
                    "id_productos", "descripcion", "precio", "talla",
                    "color", "stockActual", "fecha_ingreso", "id_proveedor"
                ]
                for i, campo in enumerate(campos):
                    self.inputs[campo].setText(str(resultado[i]) if resultado[i] is not None else "")
                QMessageBox.information(self, "Encontrado", "Producto encontrado.")
            else:
                QMessageBox.warning(self, "No encontrado", "Producto no existe.")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar: {e}")


class VerProductosTabla(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.resize(600, 400)
        self.tabla()
        self.cargar_datos()

    def tabla(self):
        layout = QVBoxLayout()

        #titulo
        titulo = QLabel("Lista de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        #tabla donde se ven los productos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Descripción", "Precio", "Talla", "Color",
            "Stock", "Fecha ingreso", "ID Proveedor"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        #boton de actualizar para que cada vez que se inserte o actualice un producto pueda verse en "ver productos"
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.cargar_datos)
        layout.addWidget(btn_actualizar)

        #boton para importar desde excel
        btn_importar = QPushButton("Importar desde Excel")
        btn_importar.clicked.connect(self.importar_excel)
        layout.addWidget(btn_importar)

        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def conectar_db(self):
        return conectar()

    def cargar_datos(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            self.tabla.setRowCount(len(productos))

            #cargar productos a la tabla
            for row_idx, producto in enumerate(productos):
                for col_idx, dato in enumerate(producto):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(dato)))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla: {e}")

    def importar_excel(self):
        try:
            # Importa el diálogo de archivos y pandas
            from PyQt6.QtWidgets import QFileDialog
            import pandas as pd

            # Abre un diálogo para seleccionar un archivo Excel
            file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx *.xls)")
            if not file_path:
                return

            # Lee el archivo Excel con pandas
            df = pd.read_excel(file_path)

            # Lista de nombres de columnas requeridas en el archivo Excel
            columnas_requeridas = [
                "ID Producto", "Descripción", "Precio", "Talla",
                "Color", "Stock", "Fecha de Ingreso", "ID Proveedor"
            ]
            
            # Normaliza nombres de columnas: minúsculas y sin espacios para no tener errores
            columnas_normalizadas = [col.lower().strip() for col in df.columns]
            requeridas_normalizadas = [c.lower() for c in columnas_requeridas]

            # Verifica que todas las columnas requeridas estén presentes en el archivo
            if not all(col in columnas_normalizadas for col in requeridas_normalizadas):
                QMessageBox.warning(
                    self,
                    "Error",
                    f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}"
                )
                return

            # Mapear nombres de columnas reales a esperados por la base de datos
            mapeo = {
                "ID Producto": "ID_Productos",
                "Descripción": "descripcion",
                "Precio": "precio",
                "Talla": "talla",
                "Color": "color",
                "Stock": "stockActual",
                "Fecha de Ingreso": "fecha_ingreso",
                "ID Proveedor": "ID_Proveedor"
            }

            # Renombra las columnas del DataFrame para que coincidan con la BD
            df = df.rename(columns={col: mapeo[col] for col in columnas_requeridas})

            conn = self.conectar_db()
            cursor = conn.cursor()

            # Itera sobre cada fila del archivo Excel
            for _, fila in df.iterrows():
                datos = (
                    str(fila["ID_Productos"]),
                    str(fila["descripcion"]),
                    float(fila["precio"]),
                    str(fila["talla"]),
                    str(fila["color"]),
                    int(fila["stockActual"]),
                    str(fila["fecha_ingreso"]),
                    str(fila["ID_Proveedor"])
                )

                # Verifica si el producto ya existe en la base de datos
                cursor.execute("SELECT * FROM productos WHERE ID_Productos = %s", (datos[0],))
                existe = cursor.fetchone()

                 # Si existe, actualiza los datos
                if existe:
                    cursor.execute(
                        """UPDATE productos SET descripcion=%s, precio=%s, talla=%s, color=%s,
                        stockActual=%s, fecha_ingreso=%s, ID_Proveedor=%s WHERE ID_Productos=%s""",
                        datos[1:] + (datos[0],)
                    )
                # Si no existe, lo inserta como nuevo
                else:
                    cursor.execute(
                        """INSERT INTO productos 
                        (ID_Productos, descripcion, precio, talla, color, stockActual, fecha_ingreso, ID_Proveedor)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        datos
                    )

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Importación completa", "Productos importados correctamente.")
            self.cargar_datos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al importar: {e}")
            

class VentanaProductosPrincipal(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(100, 100, 450, 500)
        self.principal()

    def principal(self):
        layout = QVBoxLayout()
        titulo = QLabel("Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        #botones se agregan al menu principal
        botones = [
            ("Agregar producto", lambda: self.stacked_widget.setCurrentIndex(1)),
            ("Eliminar producto", lambda: self.stacked_widget.setCurrentIndex(2)),
            ("Ver productos", lambda: self.stacked_widget.setCurrentIndex(3)),
            ("Actualizar producto", lambda: self.stacked_widget.setCurrentIndex(4)),
        ]

        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(funcion)
            btn.setFixedHeight(35)
            layout.addWidget(btn)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    ventana_inicio = VentanaProductosPrincipal(stack)
    ventana_agregar = BaseProductoVentana(stack, "Agregar Producto", "guardar", "Guardar", mostrar_buscar=False)
    ventana_eliminar = BaseProductoVentana(stack, "Eliminar Producto", "eliminar", "Eliminar")
    ventana_ver = VerProductosTabla(stack)
    ventana_actualizar = BaseProductoVentana(stack, "Actualizar Producto", "actualizar", "Actualizar")

    stack.addWidget(ventana_inicio)
    stack.addWidget(ventana_agregar)
    stack.addWidget(ventana_eliminar)
    stack.addWidget(ventana_ver) 
    stack.addWidget(ventana_actualizar)

    stack.show()
    sys.exit(app.exec())
