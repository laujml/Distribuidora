import mysql.connector
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

class BaseProveedorVentana(QWidget):
    def __init__(self, stacked_widget, titulo, accion, boton_texto):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.titulo_texto = titulo
        self.accion = accion
        self.boton_texto = boton_texto
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #4d5a62; color: white;")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(14)

        titulo = QLabel(self.titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 9px;")
        layout.addWidget(titulo)

        self.inputs = {}
        campos = [
            ("id_proveedor", "ID del Proveedor"),
            ("proveedor", "Proveedor"),
            ("p_contacto", "Nombre del Contacto"),
            ("correo", "Correo Electrónico"),
            ("telefono", "Teléfono"),
            ("direccion_proveedor", "Dirección")
        ]

        for campo, texto in campos:
            label = QLabel(texto)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-weight: 600; margin-bottom: 6px; font-size: 14px;")
            edit = QLineEdit()
            edit.setPlaceholderText(texto)
            edit.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 14px;
                color: black;
            """)
            edit.setFixedWidth(320)
            edit.setMinimumHeight(30)
            input_layout = QHBoxLayout()
            input_layout.addStretch()
            input_layout.addWidget(edit)
            input_layout.addStretch()
            layout.addWidget(label)
            layout.addLayout(input_layout)
            self.inputs[campo] = edit

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(14)

        btn_accion = QPushButton(self.boton_texto)
        btn_accion.clicked.connect(self.ejecutar_accion)
        btn_accion.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        btn_accion.setMinimumWidth(100)
        btn_accion.setFixedHeight(35)
        botones_layout.addWidget(btn_accion)

        if self.accion in ["actualizar", "eliminar"]:
            btn_buscar = QPushButton("Buscar")
            btn_buscar.clicked.connect(self.consultar_proveedor)
            btn_buscar.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
            btn_buscar.setMinimumWidth(100)
            btn_buscar.setFixedHeight(35)
            botones_layout.addWidget(btn_buscar)

        btn_otro = QPushButton(f"{self.boton_texto} otro proveedor")
        btn_otro.clicked.connect(self.limpiar_campos)
        btn_otro.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        btn_otro.setMinimumWidth(100)
        btn_otro.setFixedHeight(35)
        botones_layout.addWidget(btn_otro)

        layout.addSpacing(50)
        layout.addLayout(botones_layout)

        btn_regresar = QPushButton("Regresar")
        btn_regresar.clicked.connect(self.volver_inicio)
        btn_regresar.setStyleSheet("background-color: white; color: black; border-radius: 12px; padding: 8px 18px; font-size: 14px;")
        btn_regresar.setFixedWidth(130)
        btn_regresar.setMinimumHeight(35)
        layout.addWidget(btn_regresar, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def conectar_db(self):
        return mysql.connector.connect(host="localhost", user="root", password="1234", database="distribuidora")

    def limpiar_campos(self):
        for input in self.inputs.values():
            input.clear()

    def volver_inicio(self):
        self.limpiar_campos()
        self.stacked_widget.setCurrentIndex(0)

    def ejecutar_accion(self):
        if self.accion == "guardar":
            self.guardar_proveedor()
        elif self.accion == "actualizar":
            self.actualizar_proveedor()
        elif self.accion == "eliminar":
            self.eliminar_proveedor()

    def guardar_proveedor(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO proveedor (id_proveedor, proveedor, p_contacto, correo, telefono, direccion_proveedor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = tuple(self.inputs[c].text() for c in self.inputs)
            cursor.execute(sql, values)
            conn.commit()
            QMessageBox.information(self, "Éxito", "Proveedor guardado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def actualizar_proveedor(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = """
                UPDATE proveedor SET proveedor=%s, p_contacto=%s, correo=%s, telefono=%s, direccion_proveedor=%s
                WHERE id_proveedor=%s
            """
            values = (
                self.inputs["proveedor"].text(),
                self.inputs["p_contacto"].text(),
                self.inputs["correo"].text(),
                self.inputs["telefono"].text(),
                self.inputs["direccion_proveedor"].text(),
                self.inputs["id_proveedor"].text(),
            )
            cursor.execute(sql, values)
            conn.commit()
            QMessageBox.information(self, "Actualizado", "Datos actualizados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar: {e}")

    def eliminar_proveedor(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (self.inputs["id_proveedor"].text(),))
            conn.commit()
            QMessageBox.information(self, "Eliminado", "Proveedor eliminado correctamente.")
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar: {e}")

    def consultar_proveedor(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT proveedor, p_contacto, correo, telefono, direccion_proveedor FROM proveedor WHERE id_proveedor = %s", (self.inputs["id_proveedor"].text(),))
            resultado = cursor.fetchone()
            if resultado:
                keys = ["proveedor", "p_contacto", "correo", "telefono", "direccion_proveedor"]
                for k, v in zip(keys, resultado):
                    self.inputs[k].setText(v)
                QMessageBox.information(self, "Consulta exitosa", "Proveedor encontrado.")
            else:
                QMessageBox.warning(self, "No encontrado", "Proveedor no registrado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al consultar: {e}")
