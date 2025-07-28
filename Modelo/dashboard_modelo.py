# Uso de Modelo.db
# Conexion a la base y realizacion de consultas sql para operaciones de obtener ingresos y obtener estado de inventario.
# Requiere que se hagan las respectivas configuraciones en db_configuracion
from Modelo.db_config import conectar

#Obtiene el total de ingresos (suma de pedidos pagados) de un dia en especifico.
def obtener_ingresos_dia(dia):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total) FROM Pedido, Estado e
        WHERE DATE(fecha_hora) = %s AND e.estado = "Pagado"
    """, (dia,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado or 0.0

#Función que obtiene el inventario actual (stock) de los primeros productos, ordenados por nombre.
def obtener_estado_inventario(limit=5):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT descripcion, stockActual FROM Productos
        ORDER BY descripcion ASC
        LIMIT %s
    """, (limit,))
    productos = cursor.fetchall()
    conn.close()
    return productos
