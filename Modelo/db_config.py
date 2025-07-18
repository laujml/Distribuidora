# modelo/db_config.py
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", #poner la contraseña de su gestor de DB
        database="Distribuidora"
    )
