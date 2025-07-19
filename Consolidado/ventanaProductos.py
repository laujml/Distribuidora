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
        self.stacked_widget = stacked_widget
        self.accion = accion
        self.titulo_texto = titulo
        self.boton_texto = boton_texto
        self.mostrar_buscar = mostrar_buscar
        self.initUI()

    def initUI(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        titulo = QLabel(self.titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titulo)

        self.inputs = {}

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

        botones_layout = QHBoxLayout()

        btn_accion = QPushButton(self.boton_texto)
        btn_accion.clicked.connect(self.ejecutar_accion)
        botones_layout.addWidget(btn_accion)

        if self.mostrar_buscar and self.accion != "buscar":
            btn_buscar = QPushButton("Buscar")
            btn_buscar.clicked.connect(self.buscar_producto)
            botones_layout.addWidget(btn_buscar)

        btn_otro = QPushButton(f"{self.boton_texto} otro producto")
        btn_otro.clicked.connect(self.limpiar_campos)
        botones_layout.addWidget(btn_otro)

        layout.addLayout(botones_layout)

        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_inicio)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll_area.setWidget(content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def conectar_db(self):
        return conectar()

    def limpiar_campos(self):
        for input in self.inputs.values():
            input.clear()

    def volver_inicio(self):
        self.limpiar_campos()
        self.stacked_widget.setCurrentIndex(0)

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
            id_producto = self.inputs["id_productos"].text()
            if not id_producto:
                QMessageBox.warning(self, "Campo vacío", "Ingresa el ID del producto.")
                return
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
            sql = """UPDATE productos SET descripcion=%s, precio=%s, talla=%s, color=%s, 
                     stockActual=%s, fecha_ingreso=%s, ID_Proveedor=%s 
                     WHERE ID_Productos=%s"""
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
            id_producto = self.inputs["id_productos"].text()
            if not id_producto:
                QMessageBox.warning(self, "Campo vacío", "Ingresa el ID del producto.")
                return
            sql = "SELECT * FROM productos WHERE ID_Productos = %s"
            cursor.execute(sql, (id_producto,))
            resultado = cursor.fetchone()
            if resultado:
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
        self.setWindowTitle("Ver Productos")
        self.resize(600, 400)
        self.initUI()
        self.cargar_datos()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("Lista de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Descripción", "Precio", "Talla", "Color",
            "Stock", "Fecha ingreso", "ID Proveedor"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def conectar_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="distribuidora"
        )

    def cargar_datos(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            self.tabla.setRowCount(len(productos))

            for row_idx, producto in enumerate(productos):
                for col_idx, dato in enumerate(producto):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(dato)))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla: {e}")


class VentanaProductosPrincipal(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(100, 100, 450, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        titulo = QLabel("Gestión de Productos")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

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
