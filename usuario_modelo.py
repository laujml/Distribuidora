# modelo/usuario_modelo.py
from modelo.db_config import conectar

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

def obtener_nuevo_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID_Usuario) FROM Usuario")
    max_id = cursor.fetchone()[0]
    return (max_id or 0) + 1

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


def modificar_usuario(usuario, nueva_clave):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Usuario SET password=%s WHERE nombreUsuario=%s",
        (nueva_clave, usuario)
    )
    conn.commit()
    conn.close()



def eliminar_usuario(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuario WHERE nombreUsuario=%s", (usuario,))
    conn.commit()
    conn.close()

