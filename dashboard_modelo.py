# modelo/dashboard_modelo.py
from modelo.db_config import conectar

def obtener_ingresos_dia(dia):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total) FROM Pedido
        WHERE DATE(fecha_hora) = %s AND estado LIKE 'Pagado'
    """, (dia,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado or 0.0

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
