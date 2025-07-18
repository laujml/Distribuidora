import sys
import mysql.connector
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt6.QtCore import Qt
from estilos import Styles  


class VentanaProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Productos")
        self.setMinimumSize(600, 500)
        self.setLayout(self.initUI())

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        titulo = QLabel("Gestión de Productos")
        titulo.setObjectName("primerLabel")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.inputs = {}
        campos = ["Código", "Descripción", "Precio Unitario", "Stock"]
        for campo in campos:
            label = QLabel(campo)
            edit = QLineEdit()
            edit.setPlaceholderText(campo)
            self.inputs[campo.lower().replace(" ", "_")] = edit
            layout.addWidget(label)
            layout.addWidget(edit)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        btn_agregar = QPushButton("Agregar producto")
        btn_agregar.clicked.connect(self.agregar_producto)

        btn_eliminar = QPushButton("Eliminar producto")
        btn_eliminar.clicked.connect(self.eliminar_producto)

        btn_actualizar = QPushButton("Actualizar producto")
        btn_actualizar.clicked.connect(self.actualizar_producto)

        btn_importar = QPushButton("Importar desde Excel")
        btn_importar.clicked.connect(self.importar_excel)

        for btn in [btn_agregar, btn_eliminar, btn_actualizar, btn_importar]:
            botones_layout.addWidget(btn)

        layout.addLayout(botones_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Código", "Descripción", "Precio Unitario", "Stock"])
        layout.addWidget(self.tabla)

        self.cargar_tabla()

        return layout

    def conectar_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="distribuidora"
        )

    def limpiar_campos(self):
        for input in self.inputs.values():
            input.clear()

    def cargar_tabla(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, descripcion, precio_unitario, stock FROM producto")
            resultados = cursor.fetchall()

            self.tabla.setRowCount(0)
            for fila, datos in enumerate(resultados):
                self.tabla.insertRow(fila)
                for col, valor in enumerate(datos):
                    self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla: {e}")

    def agregar_producto(self):
        try:
            datos = (
                self.inputs["codigo"].text(),
                self.inputs["descripcion"].text(),
                float(self.inputs["precio_unitario"].text()),
                int(self.inputs["stock"].text())
            )

            if not all(datos):
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
                return

            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = "INSERT INTO producto (codigo, descripcion, precio_unitario, stock) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, datos)
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.cargar_tabla()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar: {e}")

    def eliminar_producto(self):
        codigo = self.inputs["codigo"].text()
        if not codigo:
            QMessageBox.warning(self, "Campo requerido", "Ingrese el código del producto.")
            return

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producto WHERE codigo = %s", (codigo,))
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Eliminado", "Producto eliminado correctamente.")
            self.cargar_tabla()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar: {e}")

    def actualizar_producto(self):
        try:
            datos = (
                self.inputs["descripcion"].text(),
                float(self.inputs["precio_unitario"].text()),
                int(self.inputs["stock"].text()),
                self.inputs["codigo"].text()
            )

            if not all(datos):
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
                return

            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = "UPDATE producto SET descripcion=%s, precio_unitario=%s, stock=%s WHERE codigo=%s"
            cursor.execute(sql, datos)
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Actualizado", "Producto actualizado correctamente.")
            self.cargar_tabla()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar: {e}")

    def importar_excel(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx *.xls)")
            if not file_path:
                return

            df = pd.read_excel(file_path)

            columnas_requeridas = ["codigo", "descripcion", "precio_unitario", "stock"]
            if not all(col in df.columns.str.lower() for col in columnas_requeridas):
                QMessageBox.warning(self, "Error", "El archivo debe contener las columnas: codigo, descripcion, precio_unitario, stock")
                return

            conn = self.conectar_db()
            cursor = conn.cursor()

            for _, fila in df.iterrows():
                codigo = str(fila["codigo"])
                descripcion = str(fila["descripcion"])
                precio = float(fila["precio_unitario"])
                stock = int(fila["stock"])

                # Verificar si el producto ya existe
                cursor.execute("SELECT * FROM producto WHERE codigo = %s", (codigo,))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute(
                        "UPDATE producto SET descripcion=%s, precio_unitario=%s, stock=%s WHERE codigo=%s",
                        (descripcion, precio, stock, codigo)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO producto (codigo, descripcion, precio_unitario, stock) VALUES (%s, %s, %s, %s)",
                        (codigo, descripcion, precio, stock)
                    )

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Importación completa", "Productos importados correctamente.")
            self.cargar_tabla()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al importar: {e}")
