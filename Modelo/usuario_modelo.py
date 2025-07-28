# Uso de Modelo.db_config
# Modulo que contiene la validacion de credenciales, eliminacion, modificacion, agregar, obtener id y usuario
from Modelo.db_config import conectar

#Funcion para obtener todos los usuarios registrados usando sql
def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()
    conn.close()

    return {
        u["nombreUsuario"]: {
            "password": u["password"],
            "rol": u["tipoUsuario"]
        } for u in usuarios
    }

#Funcion para obtener el siguiente ID disponible que se le puede brindar
def obtener_nuevo_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID_Usuario) FROM Usuario")
    max_id = cursor.fetchone()[0]
    return (max_id or 0) + 1

#Funcion para agregar un nuevo usuario a la base de datos
def agregar_usuario(usuario, clave, rol):
    conn = conectar()
    cursor = conn.cursor()
    nuevo_id = obtener_nuevo_id(conn)
    cursor.execute(
        "INSERT INTO Usuario (ID_Usuario, nombreUsuario, password, tipoUsuario) VALUES (%s, %s, %s, %s)",
        (nuevo_id, usuario, clave, rol)
    )
    conn.commit()
    conn.close()

#Funcion que modifica la password de un usuario 
def modificar_usuario(usuario, nueva_clave):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Usuario SET password=%s WHERE nombreUsuario=%s",
        (nueva_clave, usuario)
    )
    conn.commit()
    conn.close()

#Funcion que elimina un usuario
def eliminar_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuario WHERE nombreUsuario=%s", (usuario,))
    conn.commit()
    conn.close()

#Funcion que valida si el usuario y la password coinciden con los registrados
def validar_credenciales(usuario, clave):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuario WHERE nombreUsuario = %s AND password = %s", (usuario, clave))
    usuario_encontrado = cursor.fetchone()
    conn.close()

    if usuario_encontrado:
        return True, usuario_encontrado  
    return False, None
