# Configuracion de la conexion a la base de datos. Debe llenar con su propia password de su gestor. De lo contrario se advierte la falla de las solicitudes sql
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", #poner la contraseña de su gestor de DB
        database="Distribuidora"
    )
