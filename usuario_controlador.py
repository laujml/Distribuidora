# controlador/usuario_controlador.py
from modelo.usuario_modelo import (
    obtener_usuarios,
    agregar_usuario,
    modificar_usuario,
    eliminar_usuario
)

def login_usuario(nombre, clave):
    usuarios = obtener_usuarios()
    if nombre in usuarios and usuarios[nombre]["password"] == clave:
        return True, usuarios[nombre]["rol"]
    return False, None

def registrar_nuevo_usuario(nombre, clave, rol):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        return False 
    agregar_usuario(nombre, clave, rol)
    return True

def cambiar_contrasena(nombre, nueva_clave):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        modificar_usuario(nombre, nueva_clave)
        return True
    return False

def eliminar_usuario_existente(nombre):
    usuarios = obtener_usuarios()
    if nombre in usuarios:
        eliminar_usuario(nombre)
        return True
    return False
