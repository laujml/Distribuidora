# modelo/db_config.py
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Esen2025",
        database="Distribuidora"
    )
