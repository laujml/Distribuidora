# Uso de Modelo.usuario_controlador
# Gestiona las operaciones de autenticación y administración de usuarios, como login, registro, cambio de contraseña y eliminación
from Modelo.usuario_modelo import (
    obtener_usuarios,
    agregar_usuario,
    modificar_usuario,
    eliminar_usuario
)
# Función que valida el login del usuario con nombre y clave
def login_usuario(nombre, clave):
    usuarios = obtener_usuarios()
    if nombre in usuarios and usuarios[nombre]["password"] == clave:
        return True, usuarios[nombre]
    return False, None
# Función para registrar un nuevo usuario si no existe ya uno con ese nombre
def registrar_nuevo_usuario(nombre, clave, rol):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        return False 
    agregar_usuario(nombre, clave, rol)
    return True
# Función para cambiar la contraseña de un usuario
def cambiar_contrasena(nombre, nueva_clave):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        modificar_usuario(nombre, nueva_clave)
        return True
    return False
# Función para eliminar un usuario existente
def eliminar_usuario_existente(nombre):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        eliminar_usuario(nombre)
        return True
    return False

